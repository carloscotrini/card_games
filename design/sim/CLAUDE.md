# design/sim/

Simulation + game-theory harness for **playtesting Dodeca** (see
[`../dodeca-rules.md`](../dodeca-rules.md)). Pure Python 3, no third-party dependencies.

## Contents

- [`dodeca.py`](dodeca.py) — the **game engine** (v0.1 rules): card model, the suit ring,
  `resolve()`, and `play_match()` with the tuning dials (`win_target`, `neutral_mode`)
  exposed as parameters.
- [`players.py`](players.py) — **heuristic bots**: `RandomBot`, `HighCardBot`,
  `OneSuitBot`, `CounterBot` (counts + conserves), `MaxProbBot` (counts, no conserve),
  `CounterPushBot` (honest push), `BluffPushBot` (push + bluff/bluff-catch).
- [`simulate.py`](simulate.py) — **heuristic harness**: round-robin (seat-swapped),
  seat-fairness mirrors, skill-vs-luck, push value, and tuning sweeps. Writes
  `results.json` / `last_run.txt`. *(Kept as a baseline; superseded for the depth
  question by the equilibrium analysis.)*
- [`equilibrium.py`](equilibrium.py) — **regret-matching (CFR) solver + exact
  best-response** analysis. Module A solves the one-round reveal; Module B solves
  multi-round endgames by backward-induction CFR and measures how exploitable the
  heuristics are. Writes `equilibrium_results.json` / `equilibrium_last_run.txt`.

## How to run

```
python3 simulate.py    --matches 1500          # heuristic round-robin + sweeps
python3 equilibrium.py --a-trials 3000 --b-endgames 400   # equilibrium / exploitability
```

## Why two harnesses

Dodeca is a two-player, simultaneous-move, **imperfect-information** zero-sum game, so
optimal play is a *mixed* strategy. Value-based RL (e.g. DQN) learns a *deterministic*
policy, which is exploitable in this game class and unstable under self-play — so we use
**regret matching** (converges to a Nash equilibrium for two-player zero-sum games)
instead. The heuristic harness gives a hidden-hand, full-game baseline; the equilibrium
harness gives exact known-hand answers about mixing, fairness, and exploitability. The
conclusions live in [`../playtest-01-dodeca.md`](../playtest-01-dodeca.md).
