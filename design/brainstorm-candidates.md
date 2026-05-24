# Brainstorm 01 — candidate concepts for our first game

**Goal:** design our *first* original two-player game — easy to play, easy to learn
(rules teachable in roughly five minutes), with real but not overwhelming strategy.

**Method:** four parallel design tracks, each told to honour the
[12-point design checklist](../research/design-theory/principles.md#design-checklist)
and the [scope constraints](../CLAUDE.md) (two players, one standard 52-card deck, no
jokers/stripping). Each track pursued a different lineage from our
[research shortlist](../research/CLAUDE.md#shortlist-for-playtesting):

1. **Simultaneous-bid mind game** (Goofspiel/GOPS lineage).
2. **Trick-taking + commitment/closing** (Schnapsen + German Whist).
3. **Capture / layered scoring** (Scopa + Cribbage).
4. **Minimalist intransitive bluff** (wildcard — maximum elegance).

This report summarises the four candidates, scores them, and recommends the one we
take forward. The recommended game's full rules live in
[`dodeca-rules.md`](dodeca-rules.md).

---

## Candidate A — REBATE (simultaneous-bid)

*A GOPS-style bidding duel where winning by a large margin pays a card back to your
opponent, so crushing wins fuel their comeback.*

- **Core:** Each player holds a full suit (1–13) as bidding cards; a third suit is
  flipped one card at a time as the prize. Both bid a card face-down, high bid takes
  the prize, both bids are spent. **Twist:** the winner hands the loser a "rebate"
  card (from a shared bank) sized to the *margin* of victory — win by a lot, arm your
  opponent a lot. Most prize-points after 13 rounds wins.
- **Depth lever:** *margin management* — you want to win by the smallest possible
  amount, which is exactly what a defender can snipe.
- **Strength:** built on the most-validated skeleton we found (GOPS is Nash-solved,
  one-minute teach, symmetric → no first-player problem); the rebate is an elegant
  built-in catch-up engine.
- **Key risk:** the margin→rebate lookup adds per-round arithmetic friction; "what do
  I hand over?" can slow play and confuse beginners.

## Candidate B — THRESHOLD (trick-taking + commitment)

*A two-phase trick game where you secretly bet how many of the remaining tricks you can
win, then must live with the number.*

- **Core:** Deal 8 each, trump indicator, 34-card stock. Phase 1 plays loose
  (no follow-suit) while drawing from stock, German-Whist-style. At any point a player
  **calls Threshold**, freezing the stock and locking a secret target *T* ("I'll win at
  least T of the remaining tricks"); play switches to strict follow-suit. Opponent's only
  lever is to **double** the stakes. Score for meeting/missing T; first to 7 match points.
- **Depth lever:** the *closing* decision — convert a fuzzy probability problem into a
  countable one exactly when you think the count favours you.
- **Strength:** the strongest, most genuine commitment decision of the four; deep.
- **Key risk:** clearly the **heaviest** to teach — two phases, a hidden numeric bet, a
  doubling token, a passivity-default rule, and a scoring cap. Likely over the
  five-minute budget; better as a *later, ambitious* design than our first.

## Candidate C — TITHE (capture / layered scoring)

*A Scopa-style sum-capture game with four scoring categories, where the cards that win
one category poison another.*

- **Core:** Capture table cards whose ranks **sum** to your played card. Score four
  ways — most cards (Hoard), longest run (Spread), most of a named suit (Prime) — minus
  a **Tithe** penalty for holding duplicate ranks. You can't maximise all four at once.
- **Depth lever:** *shape tension* — greed spikes the duplicate penalty, so grabbing
  everything sabotages you.
- **Strength:** the richest scoring texture; the self-poisoning greed is genuinely clever.
- **Key risk:** **arithmetic-heavy** (constant "do these sum?" scanning) *and*
  four-category scoring — the highest total complexity of the four. Against an
  "easy to learn" brief, that's a strike.

## Candidate D — DODECA (minimalist intransitive bluff) ★ recommended

*A simultaneous-flip duel where suits beat each other in a ring; every trick is a hidden
rock-paper-scissors bet, and the discard pile is a running count.*

- **Core:** Deal 6 each. Each round both play one card face-down and flip together.
  Suits form an intransitive **ring** — adjacent suits beat each other (rank ignored);
  same-suit or "opposite" suits fall through to **high rank**. Winner banks a point,
  both cards are discarded face-up (a live count), refill to 6. A **push** lets either
  player double a trick (opponent folds or accepts). First to 7 points wins.
- **Depth lever:** a load-bearing **intransitive core** (no suit dominates) + hidden
  simultaneous commit (yomi) + an opening face-up count (German-Whist-style) + a push
  (Schnapsen-style commitment) — three depth levers from almost no rules.
- **Strength:** by far the **lowest complexity** and the **most original** — it is
  recognisably *our* idea, not a reskin. Symmetric, so no first-player fix needed.
- **Key risk:** the suit ring must be memorised (fixed below with an alphabetical
  mnemonic), and "opposite-suit" rounds collapse to pure rank (a tuning dial, noted in
  the rules).

---

## Evaluation matrix

Scored against the brief (easy to learn/play + some strategy) and the design checklist.
**L / M / H** = low / medium / high; for *Teach time* and *Overhead*, **lower is better**.

| Criterion                  | A · Rebate | B · Threshold | C · Tithe | D · Dodeca |
|----------------------------|:----------:|:-------------:|:---------:|:----------:|
| Teach time (lower better)  |     L      |      H        |    M–H    |   **L**    |
| Per-turn overhead (lower)  |     M      |      M        |    H      |   **L**    |
| Originality                |     M      |      M        |    H      |   **H**    |
| Depth ceiling              |     M      |    **H**      |    H      |    M–H     |
| First-player advantage     | none (sym) | fixed (rules) | fixed     | none (sym) |
| Commitment decision        |     M      |    **H**      |    M      |    M       |
| Intransitivity (RPS)       |     M      |      M        |    M      |   **H**    |
| Catch-up / anti-snowball   |   **H**    |      M        |    M      |    M       |
| Fit to "easy first game"   |    Good    |    Weak       |   Fair    |  **Best**  |

## Recommendation

**Take DODECA forward as our first game**, with the runner-up **REBATE** held in reserve.

Rationale:

- **It fits the brief best.** The user asked for *easy to play, easy to learn, with some
  strategy* — not a brain-burner. Dodeca has the smallest ruleset of the four and the
  lowest per-turn overhead (no arithmetic), yet still delivers meaningful decisions every
  round.
- **It is the most "ours."** The intransitive suit-ring is a genuinely original engine,
  not a thin reskin of an existing game — which is the stated end goal of the project.
- **It still fuses our three validated depth levers** (the
  [working direction](CLAUDE.md)): simultaneous bidding (GOPS), counting from a face-up
  discard pile (German Whist), and a commitment/push (Schnapsen) — just routed through a
  novel core.
- **It's symmetric**, so first-player advantage needs no special fix (checklist #4 for
  free), and it's trivially fast to prototype and playtest tonight.

**Threshold** and **Tithe** are deliberately *not* discarded — both have higher depth
ceilings and are strong candidates for a more ambitious *second* design once we've
validated our playtest loop on something light. **Rebate** is the safe fallback if
Dodeca's intransitive core fails to hold up in testing: it has a proven skeleton and the
best catch-up engine of the four.

Full rules for the chosen game: [`dodeca-rules.md`](dodeca-rules.md).
