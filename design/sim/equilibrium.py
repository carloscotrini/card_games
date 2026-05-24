"""Equilibrium / best-response analysis for Dodeca (pure Python, no deps).

Dodeca is a two-player, simultaneous-move, imperfect-information, zero-sum game, so
"optimal play" is a *mixed* (randomized) Nash equilibrium, not a deterministic policy.
This module computes equilibria with **regret matching** (the CFR update; provably
converges to a Nash equilibrium of a two-player zero-sum game) and measures how
exploitable our heuristic bots are via **exact best response**.

We analyse two tractable, faithful slices of the game:

  Module A  one-round reveal with both hands known   -> per-decision equilibrium
  Module B  multi-round endgame with both hands known -> sequential equilibrium + BR

Both use *known hands* (we hand both players their cards). That is a deliberate
simplification: it is an UPPER BOUND on the skill the suit-ring makes accessible, because
it lets a player react to the opponent's actual suits. The hidden-hand stochastic game
(see the heuristic harness) is the lower bound. The gap between them measures how much
Dodeca's hidden, simultaneous structure suppresses the ring's depth.

Scope notes: payoffs are trick differential (+1 win / -1 loss / 0 tie per reveal); the
stock/draw and the push are out of scope for these exact solves and are discussed
qualitatively in the write-up.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from functools import lru_cache

from dodeca import ALL_CARDS, resolve

SUPPORT_EPS = 0.02  # prob below this is treated as "not in the support"


# --------------------------------------------------------------------------- #
# Regret-matching solver for a two-player zero-sum matrix game.                #
# A[i][j] is the row player's payoff; the column player gets -A[i][j].         #
# Returns (game_value, row_strategy, col_strategy) with average strategies     #
# converging to a Nash equilibrium.                                            #
# --------------------------------------------------------------------------- #
def _regret_match(regret):
    pos = [r if r > 0 else 0.0 for r in regret]
    s = sum(pos)
    if s <= 0:
        n = len(regret)
        return [1.0 / n] * n
    return [p / s for p in pos]


def solve_zero_sum(A, iters=1500):
    m = len(A)
    n = len(A[0])
    rr = [0.0] * m
    rc = [0.0] * n
    sr_sum = [0.0] * m
    sc_sum = [0.0] * n
    for _ in range(iters):
        sr = _regret_match(rr)
        sc = _regret_match(rc)
        for i in range(m):
            sr_sum[i] += sr[i]
        for j in range(n):
            sc_sum[j] += sc[j]
        # row utilities against current column strategy
        u_r = [sum(A[i][j] * sc[j] for j in range(n)) for i in range(m)]
        v_r = sum(sr[i] * u_r[i] for i in range(m))
        for i in range(m):
            rr[i] += u_r[i] - v_r
        # column minimises row payoff, so its payoff is -A^T applied to row strat
        u_c = [-sum(A[i][j] * sr[i] for i in range(m)) for j in range(n)]
        v_c = sum(sc[j] * u_c[j] for j in range(n))
        for j in range(n):
            rc[j] += u_c[j] - v_c
    tot_r = sum(sr_sum) or 1.0
    tot_c = sum(sc_sum) or 1.0
    avg_r = [x / tot_r for x in sr_sum]
    avg_c = [x / tot_c for x in sc_sum]
    value = sum(avg_r[i] * A[i][j] * avg_c[j]
                for i in range(m) for j in range(n))
    return value, avg_r, avg_c


def support_size(strategy):
    return sum(1 for p in strategy if p > SUPPORT_EPS)


def exploited_value(row_strategy, A):
    """Value to the row player when it commits to row_strategy and the opponent best
    responds (picks the column that minimises row payoff)."""
    n = len(A[0])
    return min(sum(row_strategy[i] * A[i][j] for i in range(len(A)))
               for j in range(n))


# --------------------------------------------------------------------------- #
# Module A: one-round reveal, both hands known.                               #
# --------------------------------------------------------------------------- #
def deal(rng, k):
    deck = list(ALL_CARDS)
    rng.shuffle(deck)
    return deck[:k], deck[k:2 * k]


def module_a(trials=2000, k=5, iters=1200, seed=1):
    rng = random.Random(seed)
    values = []
    mixed = 0
    supports = []
    modal_not_top = 0
    hc_losses = []
    rand_losses = []
    for _ in range(trials):
        h0, h1 = deal(rng, k)
        A = [[float(resolve(a, b)) for b in h1] for a in h0]
        v, sr, sc = solve_zero_sum(A, iters)
        values.append(v)
        ss = support_size(sr)
        supports.append(ss)
        if ss >= 2:
            mixed += 1
        # does the equilibrium's most-played card differ from the highest-rank card?
        modal = max(range(k), key=lambda i: sr[i])
        top_rank = max(range(k), key=lambda i: h0[i][0])
        if modal != top_rank:
            modal_not_top += 1
        # exploitability of naive strategies (row), opponent best-responds
        hc = [0.0] * k
        hc[top_rank] = 1.0
        hc_losses.append(v - exploited_value(hc, A))
        rand = [1.0 / k] * k
        rand_losses.append(v - exploited_value(rand, A))
    return {
        "trials": trials, "k": k,
        "mean_value": sum(values) / trials,
        "max_abs_value": max(abs(x) for x in values),
        "pct_mixed": mixed / trials,
        "mean_support": sum(supports) / trials,
        "pct_modal_not_highest_rank": modal_not_top / trials,
        "mean_highcard_loss": sum(hc_losses) / trials,
        "mean_random_loss": sum(rand_losses) / trials,
    }


# --------------------------------------------------------------------------- #
# Module B: multi-round endgame, both hands known. Payoff = trick differential.#
# Solved by backward-induction CFR (each node is a stage game whose entries are #
# immediate result + equilibrium continuation value).                          #
# --------------------------------------------------------------------------- #
def endgame_solver():
    """Returns (eq_value, frac_mixed_nodes) computed over one endgame; uses closures
    so the lru_cache is fresh per endgame (hands are unique per deal)."""
    node_count = [0]
    mixed_count = [0]

    @lru_cache(maxsize=None)
    def eq(h0, h1):
        if not h0 or not h1:
            return 0.0
        A = [[resolve(a, b) + eq(tuple(c for c in h0 if c != a),
                                 tuple(c for c in h1 if c != b))
              for b in h1] for a in h0]
        v, sr, _ = solve_zero_sum(A, iters=600)
        node_count[0] += 1
        if support_size(sr) >= 2:
            mixed_count[0] += 1
        return v

    return eq, node_count, mixed_count


def br_vs_highcard(h_me, h_opp):
    """Exact best-response value (row = best responder) when the opponent plays the
    HighCard policy (always its highest-rank card). Positive => HighCard is exploitable
    by that many tricks."""
    @lru_cache(maxsize=None)
    def rec(me, opp):
        if not me or not opp:
            return 0.0
        oc = max(opp, key=lambda c: c[0])  # HighCard's deterministic move
        opp_rest = tuple(c for c in opp if c != oc)
        best = None
        for mc in me:
            val = resolve(mc, oc) + rec(tuple(c for c in me if c != mc), opp_rest)
            if best is None or val > best:
                best = val
        return best
    return rec(tuple(h_me), tuple(h_opp))


def module_b(endgames=250, k=4, seed=2):
    rng = random.Random(seed)
    eq_values = []
    mixed_fracs = []
    br_hc = []
    for _ in range(endgames):
        h0, h1 = deal(rng, k)
        eq, nc, mc = endgame_solver()
        v = eq(tuple(h0), tuple(h1))
        eq_values.append(v)
        if nc[0]:
            mixed_fracs.append(mc[0] / nc[0])
        br_hc.append(br_vs_highcard(h0, h1))
    return {
        "endgames": endgames, "k": k,
        "mean_eq_value": sum(eq_values) / endgames,
        "max_abs_eq_value": max(abs(x) for x in eq_values),
        "mean_frac_mixed_nodes": sum(mixed_fracs) / len(mixed_fracs),
        "mean_br_vs_highcard_tricks": sum(br_hc) / endgames,
        "pct_highcard_exploitable": sum(1 for x in br_hc if x > 0) / endgames,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-trials", type=int, default=2000)
    ap.add_argument("--b-endgames", type=int, default=250)
    ap.add_argument("--seed", type=int, default=20260524)
    args = ap.parse_args()

    out = []
    def line(s=""):
        out.append(s)

    line("=" * 70)
    line("DODECA EQUILIBRIUM / EXPLOITABILITY ANALYSIS (regret matching, exact)")
    line("=" * 70)

    line("\n[VALIDATION] solver sanity checks (known game values):")
    # Rock-paper-scissors: value 0, uniform strategy.
    rps = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    v, sr, _ = solve_zero_sum(rps, 4000)
    line(f"  RPS           value={v:+.3f} (expect 0.000), strat={[round(x,2) for x in sr]}"
         f" (expect ~0.33 each)")
    # Matching pennies: value 0.
    mp = [[1, -1], [-1, 1]]
    v2, sr2, _ = solve_zero_sum(mp, 4000)
    line(f"  MatchPennies  value={v2:+.3f} (expect 0.000), strat={[round(x,2) for x in sr2]}")
    # Dominant row: value +1, pure.
    dom = [[1, 1], [-1, 0]]
    v3, sr3, _ = solve_zero_sum(dom, 4000)
    line(f"  DominantRow   value={v3:+.3f} (expect +1.000), strat={[round(x,2) for x in sr3]}")

    line("\n[A] ONE-ROUND REVEAL, BOTH HANDS KNOWN")
    a = module_a(trials=args.a_trials)
    line(f"  trials={a['trials']}, hand size k={a['k']}")
    line(f"  mean equilibrium value      : {a['mean_value']:+.4f}   (0 => fair over random deals)")
    line(f"  max |value| over deals      : {a['max_abs_value']:.3f}")
    line(f"  deals needing a MIXED strat : {100*a['pct_mixed']:.1f}%   (support >= 2 cards)")
    line(f"  mean support size           : {a['mean_support']:.2f} cards")
    line(f"  equilibrium's top card is NOT the highest rank: {100*a['pct_modal_not_highest_rank']:.1f}%")
    line(f"  HighCard avg loss vs optimal: {a['mean_highcard_loss']:.3f} per round  (exploitability)")
    line(f"  Random   avg loss vs optimal: {a['mean_random_loss']:.3f} per round")

    line("\n[B] MULTI-ROUND ENDGAME, BOTH HANDS KNOWN (payoff = trick differential)")
    b = module_b(endgames=args.b_endgames)
    line(f"  endgames={b['endgames']}, hand size k={b['k']} (=> {b['k']} reveals)")
    line(f"  mean equilibrium value      : {b['mean_eq_value']:+.4f} tricks (0 => fair)")
    line(f"  max |value| over endgames   : {b['max_abs_eq_value']:.3f} tricks")
    line(f"  internal nodes needing MIX  : {100*b['mean_frac_mixed_nodes']:.1f}%  (sequential yomi)")
    line(f"  best-response vs HighCard   : {b['mean_br_vs_highcard_tricks']:+.3f} tricks avg")
    line(f"  endgames where HighCard is exploitable: {100*b['pct_highcard_exploitable']:.1f}%")

    line("\n" + "=" * 70)
    text = "\n".join(out)
    print(text)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "equilibrium_results.json"), "w") as f:
        json.dump({"module_a": a, "module_b": b}, f, indent=2)
    with open(os.path.join(here, "equilibrium_last_run.txt"), "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
