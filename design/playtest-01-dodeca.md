# Playtest 01 — Dodeca v0.1 (simulated)

**Method.** Since human playtesting isn't available yet, we tested Dodeca v0.1 with
simulated players. Two harnesses, both in [`sim/`](sim/CLAUDE.md), pure Python:

1. **Heuristic harness** (`simulate.py`) — full hidden-hand stochastic game, a field of
   seven bots (random → card-counting → push/bluff), round-robin with seat-swapping plus
   tuning sweeps. This is the *lower bound*: how well do reasonable rules-of-thumb do in
   the real, hidden-information game?
2. **Equilibrium harness** (`equilibrium.py`) — exact game theory. Dodeca is a
   two-player, **simultaneous-move, imperfect-information, zero-sum** game, so correct
   play is a *mixed* (randomised) Nash equilibrium. We compute equilibria with **regret
   matching** (the CFR update; provably converges to a Nash equilibrium for this game
   class) and measure heuristic exploitability with **exact best response**, on two
   tractable *known-hand* slices (one reveal; a four-reveal endgame). Known hands are an
   *upper bound*: they let a player react to the opponent's actual suits.

> **Why not DQN?** DQN learns a *deterministic* policy (`argmax Q`). In a
> simultaneous-move game a deterministic policy is exploitable by construction (the suit
> ring exists to punish predictability), and self-play makes the environment
> non-stationary, breaking convergence. Regret matching is the right tool: it represents
> mixed strategies and converges to equilibrium. (Our own
> [`principles.md`](../research/design-theory/principles.md) flags counterfactual regret
> as the method for hidden-information games.)

The solver was validated on games with known values before use: Rock–Paper–Scissors →
value 0.000, uniform `[0.33, 0.33, 0.33]`; Matching Pennies → 0.000, `[0.5, 0.5]`;
a dominant-row game → +1.000, pure. All correct.

---

## Headline finding

**Dodeca v0.1 contains a large amount of genuine strategic depth — but almost all of it
is locked behind the hidden, simultaneous information structure, so practical play
collapses toward a shallow rank race.**

- When the opponent's hand is **known**, the game is deep: equilibrium play requires
  *mixing* in ~77% of decisions, the suit-ring frequently makes a **non-top-rank card the
  best play (57%)**, and naive aggression is **catastrophically exploitable** (a best
  responder beats "always play your highest card" by **+2.66 of 4 tricks**).
- When hands are **hidden** (the actual game), you can't see which suit to counter, so
  the ring's intransitivity rarely triggers on purpose. Naive **"play your highest card"
  finishes 2nd of 7 bots (58%)**, *beating* the card-counting and push bots; counting
  buys only a thin edge (the best bot, MaxProb, beats HighCard just **52%**), and
  conservatively saving high cards actively **backfires** (Counter *loses* to HighCard,
  47%).

The **gap between these two regimes is the design problem**: Dodeca's depth exists but is
not *accessible* to players, because the one piece of information that unlocks it —
the opponent's suits — is exactly what the rules hide.

---

## Evidence

### A. Equilibrium structure (exact, regret matching)

**One-round reveal, both hands known** — 3,000 random deals, hand size 5:

| Measure | Result | Reading |
|---|---|---|
| Mean equilibrium value | **−0.003** | ≈ 0 → the game is **fair/symmetric** (no first-player problem) |
| Deals needing a **mixed** strategy | **77.4%** | the ring induces real randomization, not pure play |
| Mean strategy support | **2.76 cards** | you should usually randomize over ~3 cards |
| Equilibrium's top card is **not** the highest rank | **57.2%** | rank-greedy is wrong more often than right |
| HighCard avg loss vs optimal | **0.735 / round** | naive aggression is very exploitable *when hands are known* |
| Random avg loss vs optimal | 0.532 / round | predictable HighCard is worse than uniform random |

That HighCard is *more* exploitable than uniform random (0.735 > 0.532) is telling: its
flaw isn't weak cards, it's **predictability** — the ring punishes a known top card.

**Four-reveal endgame, both hands known** — 400 random endgames, solved by
backward-induction CFR:

| Measure | Result | Reading |
|---|---|---|
| Mean equilibrium value | **+0.043 tricks** | ≈ 0 → **fair** even sequentially |
| Internal nodes needing a **mixed** strategy | **76.8%** | pervasive sequential yomi |
| Best response vs HighCard | **+2.66 / 4 tricks** | HighCard loses ~2/3 of the endgame to a best responder |
| Endgames where HighCard is exploitable | **89.2%** | almost always |

### B. Hidden-hand reality (heuristic harness)

Round-robin of 7 bots, seat-swapped, 800 matches per pairing per seat (33,600 matches),
win target 7.

**Field strength** (win-rate vs the whole field):

| Bot | Field win-rate | What it does |
|---|---|---|
| **MaxProb** | **60.5%** | counts cards, plays highest win-probability (uses the ring), no conservation |
| **HighCard** | **58.4%** | naive — always plays its highest rank |
| CounterPush | 56.6% | MaxProb-style + honest push |
| BluffPush | 54.9% | + bluff-push / bluff-catch |
| Counter | 52.9% | counts but **conserves** high cards |
| Random | 40.4% | uniform |
| OneSuit | 26.1% | hoards one suit (degenerate) |

Key head-to-heads:

| Match-up | Result | Reading |
|---|---|---|
| Counter vs **Random** | **62.4%** | **skill clearly beats luck** |
| MaxProb vs HighCard | **52.1%** | counting beats naive aggression — but only barely |
| **Counter** vs HighCard | **46.8%** | conserving high cards **loses** to just playing them |
| CounterPush vs Counter (no push) | 52.8% | the push is worth a small, real edge (~+3%) |
| BluffPush vs CounterPush | 51.2% | bluffing adds a tiny edge (~+1%) |

Other texture: **seat fairness** is ~50% for every bot in mirror matches (max 52.1%) →
no seat advantage, matching the equilibrium value of ≈0. Endings are **decisive**: 100%
of matches reached the target, only **2.2%** of rounds tie, **0 drawn matches**.
**Comeback rate 25.5%** (winner trailed by ≥2 at some point), **0.89 lead changes/match**.
A small **intransitive cycle** does appear among the push bots
(**HighCard > CounterPush > BluffPush > HighCard**) — some rock-paper-scissors texture
survives into the hidden game, but it is modest.

**The contrast in one line:** HighCard goes from *2nd-best in the hidden field (58%)* to
*catastrophic against a hand-reading optimal opponent (loses 2.66 of 4 tricks)*. The
depth is entirely on the far side of the information wall.

### C. Tuning sweeps

- **Win target.** 5 → ~7.3 rounds, 17% comebacks; **7 → ~10.7 rounds, 26% comebacks**;
  9 → ~14.2 rounds, 31% comebacks. Target 7 is a sensible middle; raise to 9 if we want
  more lead changes and comebacks, drop to 5 for a faster filler.
- **Neutral-suit handling.** Switching neutral pairs from "rank decides" to "replay"
  lifts the **ring-decided share from 52% to 69%** (and lengthens matches to ~14 rounds).
  This is the cheapest lever to make the ring matter more — worth pairing with the v0.2
  information changes below.

---

## Verdict against the design checklist

- **Fair / no first-player advantage (✓).** Equilibrium value ≈ 0 in both slices, and
  every bot wins ~50% in mirror matches — the game is symmetric and needs no pie rule.
- **Decisive, low draw (✓).** 100% of matches reached the target, 0 drawn, only 2.2% of
  rounds tie — clean endings (checklist #12).
- **Skill beats luck, but the margin is thin (⚠).** Skill clearly beats randomness
  (62% vs Random), yet the *best* bot only edges naive aggression 52%, and counting +
  conservation actually loses to "just play high." Skill dominates *direction* but not
  *magnitude* — expert and novice play would look too similar.
- **Intransitivity: rich in theory, modest in practice (⚠).** The ring creates real RPS
  structure (77% mixed equilibria, non-top card optimal 57% of the time), but only one
  small cycle survives into hidden play. Checklist #7 ("intransitivity actually bites")
  **largely fails in practice** despite succeeding in theory.
- **Dominant-strategy stress test (⚠).** With hidden hands, "play high" is a strong,
  hard-to-punish line — near the degeneracy the checklist warns about (#5, #11). It is
  *catastrophically* exploitable in the known-hand game, so the fix is to **surface
  information, not to change the ring.**
- **Depth ceiling is high (✓, latent).** The endgame analysis shows enormous skill is
  *available* (a best responder crushes HighCard); the problem is purely accessibility.

## Recommendations for v0.2 (to make the depth accessible)

The single highest-leverage change is to **give players some information about suits
before they commit**, so the ring becomes targetable:

1. **Lead / response structure (strongest candidate).** One player leads a card face-up;
   the other responds knowing the led suit. This directly unlocks ring counters (the
   solver shows the depth is there) while keeping the deck and scoring identical. It does
   reintroduce a turn-order question → pair it with alternating the lead or a pie-style
   choice.
2. **Progressive reveal / open market.** Draw from a small face-up market instead of a
   blind stock, raising the amount of countable suit information over a game.
3. **Bigger hands.** With more cards in hand you more often *hold* the ring-counter to a
   guessed suit; cheap to test (`HAND_SIZE` in `dodeca.py`).
4. **Keep `neutral_mode='replay'` on the table.** The sweep showed it raises the share of
   ring-decided rounds; combined with (1) it would sharpen the RPS texture.

Re-run both harnesses after any v0.2 change; the target is to **shrink the gap** between
the known-hand depth and the hidden-hand outcome — i.e., make counting/yomi beat naive
aggression in the *actual* game, not just in the solved one.

## Honest limitations

- The equilibrium slices use **known hands** and ignore the **stock/draw** and the
  **push**; they bound accessible depth from above and isolate the ring's contribution.
- The heuristic bots are reasonable but not optimal; "HighCard is hard to beat" is a
  statement about *this* bot field, not a proof of dominance. A full-game best-response
  learner (NFSP / Deep CFR) would tighten the hidden-hand lower bound and is the natural
  next step if v0.2 doesn't close the gap.
- All numbers are reproducible from [`sim/`](sim/CLAUDE.md) with the seeds shown in the
  scripts; raw outputs are saved alongside as `*_results.json` / `*_last_run.txt`.
