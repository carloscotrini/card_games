"""Tests for Dodeca v0.2 (lead/response). Answers one question: does making moves
sequential within a round let skill (counting + countering) beat naive aggression in
the *hidden-hand* game -- i.e. does it unlock the depth Playtest 01 showed was latent?

Compares against the v0.1 baselines (MaxProb vs HighCard 52.1%; Counter vs Random 62.4%).
"""
from __future__ import annotations

import argparse
import json
import os
import random

from dodeca import resolve
from dodeca_v2 import (NaiveV2, RandomV2, ROSTER_V2, SmartRespV2, SmartV2,
                       play_match_v2)


def head_to_head(A, B, n, seed, **mkw):
    """A's win-rate over 2n matches (both seatings, alternating who starts as leader).
    Draws count as half."""
    rng = random.Random(seed)
    wins = 0.0
    games = 0
    for seat in (0, 1):
        for m in range(n):
            if seat == 0:
                bots = [A(rng), B(rng)]
                a_idx = 0
            else:
                bots = [B(rng), A(rng)]
                a_idx = 1
            st = play_match_v2(bots[0], bots[1], rng, start_leader=m % 2, **mkw)
            games += 1
            if st.winner == a_idx:
                wins += 1
            elif st.winner is None:
                wins += 0.5
    return wins / games


def round_robin(roster, n, seed):
    names = [c.name for c in roster]
    field = {nm: 0.0 for nm in names}
    counts = {nm: 0 for nm in names}
    matrix = {}
    for i in range(len(roster)):
        for j in range(i + 1, len(roster)):
            wr = head_to_head(roster[i], roster[j], n, seed + i * 100 + j)
            matrix[(names[i], names[j])] = wr
            field[names[i]] += wr
            field[names[j]] += (1 - wr)
            counts[names[i]] += 1
            counts[names[j]] += 1
    ranking = sorted(((nm, field[nm] / counts[nm]) for nm in names),
                     key=lambda x: -x[1])
    return ranking, matrix


def lead_fairness(n, seed):
    """Mirror a bot against an identical copy: seat0 win-rate (should be ~50% thanks to
    alternating leads) and the share of decided rounds won by the RESPONDER (the
    structural advantage of acting second)."""
    out = {}
    for cls in (NaiveV2, SmartV2):
        rng = random.Random(seed)
        seat0 = 0.0
        lead_w = resp_w = 0
        for m in range(n):
            st = play_match_v2(cls(rng), cls(rng), rng, start_leader=m % 2)
            if st.winner == 0:
                seat0 += 1
            elif st.winner is None:
                seat0 += 0.5
            lead_w += st.leader_round_wins
            resp_w += st.responder_round_wins
        tot = lead_w + resp_w or 1
        out[cls.name] = {"seat0_winrate": seat0 / n,
                         "responder_round_share": resp_w / tot}
    return out


def lead_value_known(trials, k, seed):
    """Exact known-hand structure of one lead/response round (no mixing -- perfect info
    of the led card makes the responder's reply pure). Leader plays first, responder
    sees the led card and best-responds from its own hand.

      leader_best  : max_c min_r resolve(c,r) averaged over deals -- the leader's value
                     if it could even see the responder's hand (an UPPER bound on leading).
      naive_lead   : value of leading the highest card vs a best-responding responder.
      resp_counters: how often the responder holds a card that beats a naively-led high.
    """
    from dodeca import ALL_CARDS
    rng = random.Random(seed)
    leader_best = []
    naive_lead = []
    resp_counters = 0
    for _ in range(trials):
        deck = list(ALL_CARDS)
        rng.shuffle(deck)
        h0, h1 = deck[:k], deck[k:2 * k]
        leader_best.append(max(min(resolve(c, r) for r in h1) for c in h0))
        hc = max(h0, key=lambda c: c[0])
        naive_lead.append(min(resolve(hc, r) for r in h1))
        if any(resolve(r, hc) > 0 for r in h1):
            resp_counters += 1
    return {
        "trials": trials, "k": k,
        "leader_best_value": sum(leader_best) / trials,
        "naive_lead_value": sum(naive_lead) / trials,
        "pct_responder_beats_naive_lead": resp_counters / trials,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matches", type=int, default=800)
    ap.add_argument("--seed", type=int, default=20260524)
    args = ap.parse_args()
    n = args.matches
    out = []
    def line(s=""):
        out.append(s)

    line("=" * 70)
    line(f"DODECA v0.2 (LEAD/RESPONSE) TESTS  (matches/pairing/seat={n}, seed={args.seed})")
    line("=" * 70)

    line("\n[1] ROUND-ROBIN FIELD STRENGTH (win-rate vs the field)")
    ranking, _ = round_robin(ROSTER_V2, n, args.seed)
    for nm, wr in ranking:
        line(f"    {nm:>12}: {100*wr:5.1f}%")

    line("\n[2] SKILL vs NAIVE  (the headline comparison)")
    sv = head_to_head(SmartV2, NaiveV2, n, args.seed + 7)
    sr = head_to_head(SmartRespV2, NaiveV2, n, args.seed + 8)
    sR = head_to_head(SmartV2, RandomV2, n, args.seed + 9)
    line(f"    SmartV2     vs NaiveV2 : {100*sv:.1f}%   (v0.1 MaxProb vs HighCard was 52.1%)")
    line(f"    SmartRespV2 vs NaiveV2 : {100*sr:.1f}%   (value of smart RESPONDING alone)")
    line(f"    SmartV2     vs RandomV2: {100*sR:.1f}%   (v0.1 Counter vs Random was 62.4%)")

    line("\n[3] LEAD / SEAT FAIRNESS  (mirror matches, alternating lead)")
    lf = lead_fairness(n, args.seed + 3)
    for nm, d in lf.items():
        line(f"    {nm:>8}: seat0 wins {100*d['seat0_winrate']:.1f}%   "
             f"responder won {100*d['responder_round_share']:.1f}% of decided rounds")

    line("\n[4] EXACT KNOWN-HAND STRUCTURE OF A LEAD/RESPONSE ROUND")
    lv = lead_value_known(trials=20000, k=6, seed=args.seed + 4)
    line(f"    leader best-case value (knows opp hand): {lv['leader_best_value']:+.3f}  "
         "(<=0 => even seeing the hand, leading isn't an edge)")
    line(f"    naive-lead value vs best response       : {lv['naive_lead_value']:+.3f}  "
         "(leading your highest is punished)")
    line(f"    responder holds a counter to a high lead: {100*lv['pct_responder_beats_naive_lead']:.1f}%")

    line("\n" + "=" * 70)
    text = "\n".join(out)
    print(text)

    here = os.path.dirname(os.path.abspath(__file__))
    results = {
        "round_robin": ranking,
        "skill_vs_naive": {"SmartV2_vs_NaiveV2": sv, "SmartRespV2_vs_NaiveV2": sr,
                            "SmartV2_vs_RandomV2": sR},
        "fairness": lf, "known_hand": lv,
    }
    with open(os.path.join(here, "v2_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(here, "v2_last_run.txt"), "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
