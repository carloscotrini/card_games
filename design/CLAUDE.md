# design/

Workspace for **our own two-player card game** — concepts, draft rules, and (eventually)
playtest notes.

## Contents

- [`brainstorm-candidates.md`](brainstorm-candidates.md) — **Brainstorm 01.** Four
  candidate concepts (one per design lineage: simultaneous-bid, trick-taking+commitment,
  capture/layered-scoring, minimalist intransitive bluff), scored against the brief, with
  a recommendation. **Outcome: Dodeca chosen as our first game; Rebate held as fallback.**
- [`dodeca-rules.md`](dodeca-rules.md) — **Dodeca, v0.1.** Full ruleset for the chosen
  first game: a simultaneous-flip duel built on an intransitive suit-ring, plus a push
  (commitment) lever and a face-up count. Includes tuning dials and a playtest checklist.
- [`playtest-01-dodeca.md`](playtest-01-dodeca.md) — **Playtest 01 (simulated).**
  Conclusions from the simulation + game-theory study: Dodeca has large latent depth, but
  most of it is locked behind hidden information; recommends v0.2 changes to surface suit
  information. Verdict against the design checklist.
- [`sim/`](sim/CLAUDE.md) — **simulation + game-theory harness** (pure Python): the engine,
  heuristic bots, the round-robin/sweep runner, and a regret-matching (CFR) equilibrium +
  exact best-response analyzer.

## Still to come (as work proceeds)

- A v0.2 ruleset that surfaces suit information (per the Playtest 01 recommendation), and
  a re-run of both harnesses to confirm the depth becomes accessible.

## Design inputs

- Mechanics shortlist: [`../research/CLAUDE.md`](../research/CLAUDE.md#shortlist-for-playtesting).
- Principles & checklist: [`../research/design-theory/principles.md`](../research/design-theory/principles.md#design-checklist).

## Working direction

Fuse the strongest validated depth levers on a single 52-card deck: a **simultaneous-bid
mind game** (GOPS) + a **commitment/closing decision** (Schnapsen) + **counting-driven
deduction** (German Whist), with a **pie/swap rule** to neutralize first-player advantage.

> Per the root [`CLAUDE.md`](../CLAUDE.md) discipline, add files here alongside an updated
> contents list in this file.
