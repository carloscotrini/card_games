# CLAUDE.md — project context & conventions

## What this repo is

A research-and-design project investigating **two-player card games** playable with a
**standard 52-card deck**, with the eventual goal of **designing our own** elegant
two-player game. Work proceeds in two phases: (1) survey existing games and design
theory, (2) design and iterate on an original game.

## Scope constraints (apply everywhere)

- **Two players** only.
- **Standard 52-card deck.** Stripped decks (e.g. 20/24/32/40 cards) and double decks
  must be flagged explicitly per game. Jokers only where called out.
- **No proprietary or special decks** (no Uno, no custom cards, no expansions).

## Repository structure

```
CLAUDE.md                         This file: project context + conventions.
README.md                         Human-facing landing page.
research/
  CLAUDE.md                       Research overview + cross-cutting summary + shortlist.
  existing-games/
    CLAUDE.md                     Index of the three game-survey categories.
    01-accessible-fun.md          Category 1: easy to teach, light, fun-first.
    02-simple-but-deep.md         Category 2: minimal rules, deep strategy (core interest).
    03-complex-strategic.md       Category 3: heavyweight rules + deep strategy.
  design-theory/
    CLAUDE.md                     Index of design-theory material.
    principles.md                 Game-design theory + 12-point design checklist.
design/
  CLAUDE.md                       Workspace for our own game (concepts, rules, playtests).
```

## CLAUDE.md maintenance discipline (required)

This repo treats `CLAUDE.md` files as living documentation of structure and intent.
They must be kept in sync with the actual contents. Specifically:

1. **Every folder and subfolder must contain a `CLAUDE.md`** describing its purpose and
   listing its contents. When you create a new folder, add its `CLAUDE.md` in the same
   commit.
2. **Any commit that changes the repository structure** — adding, moving, renaming, or
   removing files or folders — must update the affected `CLAUDE.md` files (and the tree
   above) in that same commit. Structure changes and `CLAUDE.md` updates ship together,
   never separately.
3. **Any major change to a document's structure** (new top-level sections, reorganized
   categories, a renamed report) must be reflected in that folder's `CLAUDE.md` and, if
   it affects the layout, in this root file's tree.
4. **Keep the tree above authoritative.** If it drifts from reality, the tree is the bug
   — fix it as part of the change that caused the drift.

When in doubt, update the `CLAUDE.md`. A structural change is not complete until its
documentation is current.
