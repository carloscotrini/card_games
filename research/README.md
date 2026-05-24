# Research overview

Landscape survey of two-player card games for a standard 52-card deck, plus design
theory to seed our own game. Four category files:

| # | Category | File | What it covers |
|---|----------|------|----------------|
| 1 | Accessible & fun | [01-accessible-fun.md](01-accessible-fun.md) | ~1-minute teach, light, fun-first |
| 2 | Simple but deep | [02-simple-but-deep.md](02-simple-but-deep.md) | Minimal rules, large strategic depth |
| 3 | Complex & strategic | [03-complex-strategic.md](03-complex-strategic.md) | Heavyweight rules + deep strategy |
| 4 | Design principles | [04-design-principles.md](04-design-principles.md) | Theory/frameworks for designing our own |

## Cross-cutting takeaways

- **The depth-to-rules sweet spot is real and well-populated.** The strongest
  "easy to learn, hard to master" two-handers are **Goofspiel/GOPS**, **Schnapsen**,
  **German Whist**, and **Cribbage** — all minimal rules, strongly skill-dominated,
  and several are academically studied or competitively played.
- **Depth comes from a few interacting mechanisms, not many rules.** Recurring
  depth engines: hidden information / deduction, the *closing/knocking* commitment
  decision, card counting over a small deck, tempo, and simultaneous-move bluffing.
- **Complexity does not guarantee depth.** Two-Handed Canasta and Honeymoon Bridge
  carry heavy rules with disproportionate luck or diluted strategy at two players.
  Piquet and Klaberjass are the complex games where the rules genuinely pay off.
- **A standard deck is a design asset.** Everyone already knows it — near-zero
  learning cost — so our design should generate depth from rule *interactions*.

## Deck requirements at a glance

- **Pure 52-card deck:** Goofspiel/GOPS, German Whist, Cribbage, Gin Rummy, Golf,
  Speed/Spit, Egyptian Ratscrew, Honeymoon Bridge, All Fours.
- **Stripped deck:** Schnapsen (20), Sixty-Six (24), Piquet/Écarté/Klaberjass (32),
  Briscola/Scopa (40).
- **Two decks / 100+ cards:** Bezique (64), Two-Handed Pinochle (48), Canasta (108), Nertz.
- **No game here requires jokers.**

## Shortlist for playtesting

Best references for our own design — minimal rules, maximal depth, single 52-card deck:

1. **Goofspiel / GOPS** — pure simultaneous-bid mind game; Nash-solved; 1-minute teach.
2. **German Whist** — counting + duck-vs-win tension from almost no rules; pure 52.
3. **Schnapsen** — the *closing* decision is the canonical depth-from-commitment lever (stripped deck).
4. **Cribbage** — two clean skill layers (discard EV + pegging); statistically studied.

These four, plus the [design checklist](04-design-principles.md#design-checklist),
are the primary inputs for our own two-player game.
