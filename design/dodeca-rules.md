# DODECA — rules (v0.1)

*A two-player duel of hidden cards where the four suits beat each other in a ring. Every
round is a simultaneous rock-paper-scissors bet: do you win by **suit** or by **rank**? —
and the cards already played are a running count you can read.*

- **Players:** 2
- **Deck:** one standard 52-card deck. No jokers, no stripping.
- **Teach time:** ~3 minutes.
- **Status:** v0.1 — first complete draft, not yet playtested. Open tuning dials are
  flagged inline and collected at the end.

---

## 1. Victory condition (read this first)

Win the **match** by being the first to bank **7 points**. A normal trick is worth
**1 point**; a *pushed* trick is worth **2** (see §6). Points come only from winning
tricks — nothing else scores. If the deck runs out before anyone reaches 7, the player
with more banked points wins; an exact tie is replayed.

## 2. The suit ring (the one rule that makes the game)

The four suits beat each other in a cycle — **alphabetical order, each suit beats the
next, and Spades wraps around to beat Clubs**:

```
        ♣ Clubs ──beats──▶ ♦ Diamonds
        ▲                        │
      beats                    beats
        │                        ▼
        ♠ Spades ◀──beats── ♥ Hearts
```

> Mnemonic: **C → D → H → S → (back to C)**. Alphabetical, each beats the next; the last
> (Spades) loops back to beat the first (Clubs).

Each suit therefore beats exactly one suit, loses to exactly one, and is **neutral**
("opposite") to the remaining one:

| Suit | Beats | Loses to | Neutral (opposite) |
|------|:-----:|:--------:|:------------------:|
| ♣    | ♦     | ♠        | ♥                  |
| ♦    | ♥     | ♣        | ♠                  |
| ♥    | ♠     | ♦        | ♣                  |
| ♠    | ♣     | ♥        | ♦                  |

No suit dominates — every suit has a predator. That intransitivity is what stops any
"always play X" strategy.

## 3. Setup

1. Shuffle the full 52-card deck.
2. Deal **6 cards** to each player (hidden hands).
3. Place the rest face-down as the **stock**.
4. Leave space for a shared face-up **discard pile** (the count) — it starts empty.

Cards rank **Ace high** down to **2** whenever rank matters (Ace, K, Q, J, 10 … 2).

## 4. Playing a round

1. **Commit.** Both players simultaneously choose one card from hand and place it
   face-down in front of them.
2. **Flip.** Both cards are turned face-up at the same time.
3. **Resolve the winner** (§5).
4. **Bank.** The winner takes the trick's points. (On a tie with no winner, see §5c.)
5. **Discard.** Both played cards go face-up to the shared discard pile — they are out of
   the game and visible to both players for counting.
6. **Refill.** Each player draws one card from the stock back up to 6 (winner draws
   first; irrelevant once the stock is low). If the stock is empty, hands simply shrink.
7. Repeat until someone reaches 7 points or both hands are empty.

## 5. Who wins the round

Compare the two flipped cards:

- **(a) Adjacent suits → the ring decides, rank is ignored.** If one card's suit *beats*
  the other's per §2 (e.g. ♥ vs ♠ → ♥ wins; ♣ vs ♠ → ♠ wins), that card wins regardless
  of rank. A ♥2 beats a ♠A.
- **(b) Same suit, or the two neutral/"opposite" suits → higher rank wins.** Two clubs →
  higher club. A club vs a heart (neutral pair) → higher rank of the two, suit ignored.
- **(c) Exact tie → no score.** Only possible on a same-suit pair of equal rank (cannot
  happen — one deck) or a neutral pair of equal rank (e.g. ♣9 vs ♥9). Both cards are
  discarded, no points, replay the round with fresh cards. *(Tuning dial: see §9.)*

> Quick decision tree per flip: **Same suit?** → higher rank. **Different suits adjacent
> in the ring?** → ring winner. **Different suits but neutral?** → higher rank.

## 6. The push (the commitment decision)

Before the flip in any round, either player may declare **"Push."**

- The opponent immediately chooses to **fold** or **accept**.
- **Fold:** the opponent concedes the round without flipping. The pusher banks **1**
  point; both committed cards are still discarded and hands refill as normal. (You pay a
  card to take a guaranteed point and to hide what you were holding.)
- **Accept:** both cards flip and resolve as normal, but the trick is now worth **2**
  points to whoever wins it.

Only one push per round. You push when you believe your committed card wins — but
declaring it warns the opponent, who may fold to deny you the double or accept to punish
a bluff. *(Tuning dial: re-push / raising to 3 is in §9.)*

## 7. Where the depth comes from

Three levers interact, all from the rules above:

- **Hidden simultaneous commit (yomi).** You're guessing which suit your opponent will
  bring. Holding "all high spades" is not strong — a low ♥ beats your ♠ on the ring,
  while a ♦ ignores your suit and forces a rank fight. Every card is *both* a
  suit-weapon (rank-proof against the suit it beats) and a rank-weapon (against its
  neutral suit). Choosing which role to play, blind, is the game.
- **The count (German-Whist-style).** The face-up discard pile shows every spent card. By
  the late rounds you can deduce much of what your opponent can still hold, so early
  bluffs harden into near-calculation.
- **The push (Schnapsen-style closing).** A safety-vs-reward lever: take a guaranteed
  point, or double down on a read and risk handing the opponent two.

## 8. Worked example

Score 5–5, late in the deck. The discard pile shows **both black Aces and the ♥A are
already gone**. You hold ♠K, ♥9, ♣3, ♦2, ♦7, ♠4.

Your opponent has been winning with hearts and likely holds a high ♥, expecting you to
answer with a spade (♥ loses to ♠). You **Push**. She **accepts** — a 2-point trick that
would win her the match.

Reading her for a high heart *and* for the bait, you do **not** play ♠K. You play **♦2**.
She, trying to out-ring your *expected* spade, plays **♠J** (♠ beats ♣, and she's hoping
to catch a spade)... but ♠ vs ♦ is the ring matchup **♦ beats ♠** — your deuce takes the
2-point trick and the match. The "bluff" was declining to use your best card in the
matchup she'd prepared for.

## 9. Open tuning dials (for playtesting)

v0.1 deliberately leaves these knobs to settle during testing:

- **Win target (7).** Try 5 (faster, swingier) or 9 (more counting) if matches feel too
  short or too long.
- **Neutral-suit rounds.** If "opposite suit → rank" rounds feel too much like flat
  high-card-wins, make a neutral pairing a **no-score replay** instead, pushing players
  toward ring matchups and sharpening the RPS texture.
- **Push economy.** Try allowing a **re-push to 3**, or capping pushes per deal, if the
  2× push proves too weak or too strong.
- **Hand size (6) / draw.** If blind draws hand out too-perfect counters, replace the
  stock draw with a small face-up **market** (draft 1 of 2), trading luck for counting.

## 10. Playtest checklist (what to measure)

Tie observations back to the [design checklist](../research/design-theory/principles.md#design-checklist)
and the Browne/Ludi quality metrics:

- [ ] **Teachable in ~3 min?** Time a first-time explanation; watch where the ring
  confuses people.
- [ ] **Skill > luck over a match?** Track the stronger player's win-rate over a 10-deal
  match; should be clearly above 50%.
- [ ] **No dominant line (checklist #5, #11).** Does any single strategy ("always push,"
  "always play neutral high cards," "hoard one suit") win repeatedly with no counter? If
  so, the intransitive core has a leak — patch via §9.
- [ ] **Intransitivity actually bites (checklist #7).** Do players visibly mind-read suit
  choices, or does it collapse to rank? If the latter, apply the neutral-suit dial.
- [ ] **Catch-up works (checklist #9).** Does a 5–2 lead still get overturned sometimes
  via pushes? Log lead-changes per match; we want several.
- [ ] **The push is a real decision (checklist #10).** Is folding-vs-accepting genuinely
  tense, or near-always obvious? If obvious, retune the push economy.
- [ ] **Quality metrics (checklist #12):** low draw rate, frequent lead changes, decisive
  endings, and enough branching that the game resists trivial solving.
