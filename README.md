# card_games

Investigating simple-yet-deeply-strategic card games playable with a **standard
52-card deck**, focused on **two-player variants**. The end goal is to design our
own elegant two-player card game.

## Layout

```
research/
  existing-games/    Surveys of real two-player games, by category
    01-accessible-fun.md     Quick to teach, light, fun-first
    02-simple-but-deep.md    "Easy to learn, hard to master" — the core interest
    03-complex-strategic.md  Heavyweight rules with deep strategy
  design-theory/     Frameworks and principles for designing games
    principles.md            Theory + a 12-point design checklist
design/              Workspace for our own two-player game (in progress)
    brainstorm-candidates.md Four candidate concepts + recommendation
    dodeca-rules.md          Dodeca v0.1 — our chosen first game
    playtest-01-dodeca.md    Simulated + game-theory study of Dodeca v0.1
    dodeca-v2-rules.md       Dodeca v0.2 — lead/response variant
    playtest-02-dodeca-v2.md Study of Dodeca v0.2 (lead/response)
    sim/                     Pure-Python engine, bots, and CFR/best-response harness
```

Each folder has a `CLAUDE.md` describing its purpose and contents; start at
[`CLAUDE.md`](CLAUDE.md) for project context and conventions, then
[`research/CLAUDE.md`](research/CLAUDE.md) for the cross-cutting research summary
and the shortlist of games worth playtesting.

## Scope constraints

- Standard 52-card deck (stripped/doubled variants noted explicitly; jokers only where flagged).
- Two players.
- No proprietary or special decks.
