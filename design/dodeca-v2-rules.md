# Dodeca v0.2 — the lead/response variant

**Status: tested, then superseded.** v0.2 was the fix proposed in
[Playtest 01](playtest-01-dodeca.md) for v0.1's core flaw (depth locked behind hidden,
simultaneous information). [Playtest 02](playtest-02-dodeca-v2.md) shows it *works* —
skill now dominates — but it **over-corrects** into a lopsided second-mover advantage. It
is a stepping stone toward v0.3, not a finished design.

## What changes from [v0.1](dodeca-rules.md)

Only the within-round turn structure. Deck (standard 52), six-card hands, the suit-ring
(C→D→H→S→C), rank tie-breaking, the face-up discard count, refill from stock, and the
race to 7 points are all **unchanged**.

- **v0.1:** both players commit a card *simultaneously*, then flip.
- **v0.2:** the round has a **leader** and a **responder**. The leader plays a card
  **face-up**; the responder, *seeing the led card*, then plays a card from their own
  (still hidden) hand. Resolve with the usual ring-then-rank rule; the winner scores 1.
- **The lead alternates every round** (player 0 leads round 1, player 1 leads round 2, …).
- **The push is removed** in v0.2, to isolate the effect of the information change. It can
  be reintroduced later (e.g. only the responder may double).

## Why this was tried

The whole point of the suit-ring is intransitivity ("rock-paper-scissors"), which only
bites when you can aim a counter at the opponent's suit. v0.1 hides every player's cards
and resolves simultaneously, so that knowledge never exists and play collapses to a rank
race. Letting the responder *see* the led card hands them exactly the information the ring
needs.

## The catch (see Playtest 02)

The ring ignores rank, so the suit that beats the led suit beats **every** card of it.
A responder therefore holds a guaranteed counter ~90% of the time, and acting second
becomes an overwhelming edge (the responder wins ~87% of decided rounds between skilled
players). Alternating the lead keeps the *match* fair, but each player's lead turn is
nearly hopeless — half the game is low-agency. The fix belongs in **v0.3** (rebalance the
lead/response asymmetry and/or restore rank relevance to the ring); see the playtest for
options.
