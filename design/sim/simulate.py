"""Dodeca playtest harness: runs simulated matches, logs metrics, prints conclusions.

Experiments:
  1. Round-robin tournament (seat-swapped) -> win matrix, look for intransitive cycles.
  2. Seat-fairness: mirror matches (a bot vs itself) -> seat win-rate, must be ~50%.
  3. Skill vs luck: Counter vs Random win-rate over many matches.
  4. Push value: CounterPush vs Counter, plus push frequency/outcome stats.
  5. Tuning sweeps: win target {5,7,9}; neutral-suit {rank, replay}; report effects.

Run:  python3 simulate.py [--matches N] [--seed S]
Writes a JSON summary to results.json next to this file and prints a report.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from collections import defaultdict

from dodeca import play_match
from players import ROSTER


def make(bot_cls, rng):
    return bot_cls(rng)


def run_pairing(a_cls, b_cls, n, seed, **kw):
    """Play n matches with A in seat0 and n with A in seat1. Return aggregate stats
    for A (wins/losses/draws) plus per-match metric accumulators."""
    rng = random.Random(seed)
    agg = defaultdict(float)
    a_wins = a_losses = draws = 0
    for direction in (0, 1):
        for _ in range(n):
            a = make(a_cls, rng)
            b = make(b_cls, rng)
            if direction == 0:
                st = play_match(a, b, rng, **kw)
                a_seat = 0
            else:
                st = play_match(b, a, rng, **kw)
                a_seat = 1
            if st.winner is None:
                draws += 1
            elif st.winner == a_seat:
                a_wins += 1
            else:
                a_losses += 1
            agg["rounds"] += st.rounds
            agg["lead_changes"] += st.lead_changes
            agg["ring_decided"] += st.ring_decided
            agg["rank_decided"] += st.rank_decided
            agg["ties"] += st.ties
            agg["pushes"] += st.pushes
            agg["push_folds"] += st.push_folds
            agg["push_accepts"] += st.push_accepts
            agg["pusher_won_points"] += st.pusher_won_points
            agg["comebacks"] += 1 if st.comeback else 0
            agg["ended_by_target"] += 1 if st.ended_by_target else 0
            agg["matches"] += 1
    return a_wins, a_losses, draws, agg


def round_robin(n, seed, **kw):
    names = [c.name for c in ROSTER]
    winrate = {a: {} for a in names}
    decisive = {}  # win-rate excluding draws
    metrics = defaultdict(float)
    for i, a_cls in enumerate(ROSTER):
        for j, b_cls in enumerate(ROSTER):
            if j <= i:
                continue
            aw, al, dr, agg = run_pairing(a_cls, b_cls, n, seed + i * 100 + j, **kw)
            total = aw + al + dr
            wr = aw / total
            winrate[a_cls.name][b_cls.name] = wr
            winrate[b_cls.name][a_cls.name] = al / total
            dec = aw / (aw + al) if (aw + al) else 0.5
            decisive[(a_cls.name, b_cls.name)] = dec
            for k, v in agg.items():
                metrics[k] += v
    return names, winrate, decisive, metrics


def fmt_pct(x):
    return f"{100 * x:5.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matches", type=int, default=1500,
                    help="matches per seat-direction per pairing")
    ap.add_argument("--seed", type=int, default=20260524)
    args = ap.parse_args()
    n, seed = args.matches, args.seed

    report = {}
    out = []
    def line(s=""):
        out.append(s)

    line("=" * 70)
    line(f"DODECA SIMULATION  (matches/pairing/seat = {n}, seed = {seed})")
    line("=" * 70)

    # ---- Experiment 1: round-robin (default rules) ----
    names, winrate, decisive, metrics = round_robin(n, seed)
    line("\n[1] ROUND-ROBIN WIN MATRIX (row's win-rate vs column, seat-averaged)")
    header = "             " + "".join(f"{nm:>11}" for nm in names)
    line(header)
    field_avg = {}
    for a in names:
        cells = []
        tot = 0.0
        cnt = 0
        for b in names:
            if a == b:
                cells.append(f"{'--':>11}")
            else:
                cells.append(f"{fmt_pct(winrate[a][b]):>11}")
                tot += winrate[a][b]
                cnt += 1
        field_avg[a] = tot / cnt
        line(f"{a:>12} " + "".join(cells))
    line("\n  Overall win-rate vs the field (higher = stronger):")
    for a in sorted(names, key=lambda x: -field_avg[x]):
        line(f"    {a:>12}: {fmt_pct(field_avg[a])}")
    report["field_winrate"] = field_avg
    report["win_matrix"] = winrate

    # intransitive cycles among the non-counting "shape" bots + counters
    line("\n  Intransitivity check (A>B>C>A cycles, using decisive win-rate):")
    cycles = []
    for a in names:
        for b in names:
            for c in names:
                if len({a, b, c}) < 3:
                    continue
                ab = decisive.get((a, b), 1 - decisive.get((b, a), 0.5))
                bc = decisive.get((b, c), 1 - decisive.get((c, b), 0.5))
                ca = decisive.get((c, a), 1 - decisive.get((a, c), 0.5))
                if ab > 0.5 and bc > 0.5 and ca > 0.5:
                    key = tuple(sorted([a, b, c]))
                    if (a, b, c) not in cycles:
                        cycles.append((a, b, c))
    seen = set()
    uniq = []
    for cyc in cycles:
        k = frozenset(cyc)
        if k not in seen:
            seen.add(k)
            uniq.append(cyc)
    if uniq:
        for a, b, c in uniq:
            line(f"    {a} > {b} > {c} > {a}")
    else:
        line("    none found (relationships are transitive)")
    report["intransitive_cycles"] = uniq

    # round/metric summary
    m = metrics
    M = m["matches"]
    decided_rounds = m["ring_decided"] + m["rank_decided"]
    line("\n  Aggregate round texture (all round-robin matches):")
    line(f"    matches simulated      : {int(M)}")
    line(f"    avg rounds / match     : {m['rounds'] / M:5.2f}")
    line(f"    avg lead changes / match: {m['lead_changes'] / M:5.2f}")
    line(f"    comeback rate (winner trailed by >=2): {fmt_pct(m['comebacks'] / M)}")
    line(f"    ended by reaching target: {fmt_pct(m['ended_by_target'] / M)}")
    if decided_rounds:
        line(f"    rounds decided by RING : {fmt_pct(m['ring_decided'] / decided_rounds)}")
        line(f"    rounds decided by RANK : {fmt_pct(m['rank_decided'] / decided_rounds)}")
    line(f"    tie (no-score) rounds  : {fmt_pct(m['ties'] / m['rounds'])} of rounds")
    report["round_texture"] = {
        "avg_rounds": m["rounds"] / M,
        "avg_lead_changes": m["lead_changes"] / M,
        "comeback_rate": m["comebacks"] / M,
        "ended_by_target": m["ended_by_target"] / M,
        "ring_share": m["ring_decided"] / decided_rounds if decided_rounds else None,
        "rank_share": m["rank_decided"] / decided_rounds if decided_rounds else None,
        "tie_share": m["ties"] / m["rounds"],
    }

    # ---- Experiment 2: seat fairness (mirror matches) ----
    line("\n[2] SEAT FAIRNESS  (mirror: a bot vs an identical copy; seat0 win-rate)")
    seat = {}
    for cls in ROSTER:
        rng = random.Random(seed + 7)
        s0 = draws = 0
        total = 2 * n
        for _ in range(total):
            a = cls(rng)
            b = cls(rng)
            st = play_match(a, b, rng)
            if st.winner == 0:
                s0 += 1
            elif st.winner is None:
                draws += 1
        seat[cls.name] = s0 / total
        line(f"    {cls.name:>12}: seat0 wins {fmt_pct(s0 / total)}  (draws {fmt_pct(draws/total)})")
    report["seat0_winrate"] = seat

    # ---- Experiment 3: skill vs luck ----
    from players import CounterBot, RandomBot, HighCardBot
    line("\n[3] SKILL vs LUCK")
    for strong, weak in [(CounterBot, RandomBot), (CounterBot, HighCardBot)]:
        aw, al, dr, _ = run_pairing(strong, weak, n, seed + 31)
        t = aw + al + dr
        line(f"    {strong.name} vs {weak.name}: {fmt_pct(aw/t)} win  (draws {fmt_pct(dr/t)})")
        report[f"skill_{strong.name}_vs_{weak.name}"] = aw / t

    # ---- Experiment 4: push value ----
    from players import CounterPushBot, BluffPushBot
    line("\n[4] PUSH VALUE & DYNAMICS")
    aw, al, dr, agg = run_pairing(CounterPushBot, CounterBot, n, seed + 41)
    t = aw + al + dr
    line(f"    CounterPush vs Counter(no push): {fmt_pct(aw/t)} win for the pusher")
    pushes = agg["pushes"]
    if pushes:
        line(f"    pushes/match: {pushes/agg['matches']:.2f}; "
             f"folds {fmt_pct(agg['push_folds']/pushes)}, "
             f"accepts {fmt_pct(agg['push_accepts']/pushes)}; "
             f"pusher banked the points {fmt_pct(agg['pusher_won_points']/pushes)} of pushes")
    report["push_counterpush_vs_counter"] = aw / t
    bw, bl, bdr, bagg = run_pairing(BluffPushBot, CounterPushBot, n, seed + 42)
    bt = bw + bl + bdr
    line(f"    BluffPush vs CounterPush(honest): {fmt_pct(bw/bt)} win for the bluffer")
    report["push_bluff_vs_honest"] = bw / bt

    # ---- Experiment 5: tuning sweeps ----
    line("\n[5] TUNING SWEEPS")
    line("  (a) Win target -> match length & comeback rate (Counter vs CounterPush field proxy)")
    sweep_targets = {}
    for wt in (5, 7, 9):
        _, _, _, mm = round_robin_metrics(n // 2, seed + 50, win_target=wt)
        Mt = mm["matches"]
        sweep_targets[wt] = {
            "avg_rounds": mm["rounds"] / Mt,
            "comeback_rate": mm["comebacks"] / Mt,
            "ended_by_target": mm["ended_by_target"] / Mt,
            "avg_lead_changes": mm["lead_changes"] / Mt,
        }
        line(f"    target={wt}: avg_rounds {mm['rounds']/Mt:5.2f}, "
             f"lead_changes {mm['lead_changes']/Mt:4.2f}, "
             f"comeback {fmt_pct(mm['comebacks']/Mt)}, "
             f"ended_by_target {fmt_pct(mm['ended_by_target']/Mt)}")
    report["sweep_win_target"] = sweep_targets

    line("\n  (b) Neutral-suit handling: 'rank' (default) vs 'replay'")
    sweep_neutral = {}
    for mode in ("rank", "replay"):
        _, _, _, mm = round_robin_metrics(n // 2, seed + 60, neutral_mode=mode)
        Mt = mm["matches"]
        dec = mm["ring_decided"] + mm["rank_decided"]
        sweep_neutral[mode] = {
            "avg_rounds": mm["rounds"] / Mt,
            "ring_share": (mm["ring_decided"] / dec) if dec else None,
            "comeback_rate": mm["comebacks"] / Mt,
        }
        ring_share = f"{100*mm['ring_decided']/dec:.1f}%" if dec else "n/a"
        line(f"    neutral={mode:>6}: avg_rounds {mm['rounds']/Mt:5.2f}, "
             f"ring-decided share {ring_share}, comeback {fmt_pct(mm['comebacks']/Mt)}")
    report["sweep_neutral"] = sweep_neutral

    line("\n" + "=" * 70)
    text = "\n".join(out)
    print(text)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(here, "last_run.txt"), "w") as f:
        f.write(text + "\n")


def round_robin_metrics(n, seed, **kw):
    """Round-robin that only aggregates metrics (for sweeps)."""
    return round_robin(n, seed, **kw)


if __name__ == "__main__":
    main()
