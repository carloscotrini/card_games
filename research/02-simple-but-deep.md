# Category 2 — Simple but deep

The "easy to learn, hard to master" sweet spot: minimal rules (start in a couple
minutes) but large strategic depth, where skill dominates luck over repeated play
and expert play looks very different from novice play. **This is the core category
for the project.**

## Strongest picks (best depth-to-rules ratio)

### 1. Schnapsen / Sixty-Six
- **2p fit:** Native; widely regarded as the best 2p trick-taker for depth-per-card.
- **Rules:** 20-card deck; win tricks to reach 66 card points, declare marriages (K+Q = 20/40), announce when you think you've won. ~5 min to learn.
- **Where the depth comes from:** The **closing** decision — at any turn you may close the stock, switching from a loose draw phase (no follow-suit) to a tight perfect-recall phase (must follow suit/trump). Closing converts a memory/probability problem into a near-solved combinatorial one, but mis-closing costs game points. Trump control, marriage timing, and counting toward 66 all interact.
- **Skill vs luck:** Heavily skill-dominated over a match. Studied seriously — Martin Tompa's *Winning Schnapsen* and his Schnapsen Log give near-rigorous endgame analysis; played competitively in Austria.
- **Learning curve:** Minutes to start; mastery is years.
- **Deck:** Stripped 20-card (A,10,K,Q,J each suit); Sixty-Six uses 24.
- Source: https://www.pagat.com/marriage/schnaps.html

### 2. Goofspiel / GOPS (Game of Pure Strategy)
- **2p fit:** Native, symmetric — arguably the purest skill game here.
- **Rules:** Each player gets one full suit (1–13); a third suit is flipped one card at a time as a "prize"; both simultaneously bid a card, high bid wins the prize, bid cards are discarded. ~1 min to learn.
- **Where the depth comes from:** Pure simultaneous-move, hidden-intention game — no hidden cards; all depth from mixed strategies, tempo, and out-guessing. Correct play is genuinely game-theoretic (randomization).
- **Skill vs luck:** No luck except prize order (a fixed-order variant removes even that). A mixed-strategy Nash equilibrium was found by Rhoads & Bartholdi (2012); the state space (~2.4×10²⁹) makes it a benchmark AI/game-theory problem.
- **Deck:** 52 (three suits used).
- Source: https://en.wikipedia.org/wiki/Goofspiel

### 3. German Whist
- **2p fit:** Native 2p adaptation of Whist; often cited as the best "easy/hard" 52-card 2p game.
- **Rules:** 13 cards each; turn up a stock card, trick winner takes it (loser draws blind) for 13 tricks; then play out the hand you built — only second-phase tricks score. ~3 min to learn.
- **Where the depth comes from:** Phase one is a tension between *winning* a desirable face-up card now versus *ducking* to take an unknown card and conserve high cards/trumps. Pure card counting: by phase two an expert knows almost the entire opponent hand. Trump management and deliberate trick-sacrifice for position drive expert play.
- **Skill vs luck:** Strongly skill-favoring; counting and tempo decide most games.
- **Deck:** 52.
- Source: https://www.pagat.com/whist/german_whist.html

### 4. Cribbage
- **2p fit:** Native 2p (the canonical form); board-and-peg.
- **Rules:** Discard 2 of 6 to the dealer's "crib," peg during play to 31, then count hands (15s, pairs, runs, flushes). Starts in minutes.
- **Where the depth comes from:** Two distinct skill layers — *discard* (expected-value optimization of your hand vs. the crib, factoring whose crib it is) and *pegging* (sequence/trap play with hidden cards). Heavily statistical; strong players win ~65–70%.
- **Skill vs luck:** Real luck (cut, deal) but skill clearly dominates long-run; ACC tournaments.
- **Deck:** 52.
- Source: https://www.cribbage.org/NewSite/tips/rasmussenskill.asp

## Strong supporting candidates

- **Piquet** — Native 2p, 32-card deck, 12 each + 8 talon; three scoring layers (exchange, declarations of point/sequence/set, then tricks). Declarations leak information, so by trick play you can deduce most of the opponent's hand. Higher rules-overhead but huge depth (see also [category 3](03-complex-strategic.md)). https://www.pagat.com/notrump/piquet.html
- **Briscola (2p)** — Native, simple (40-card deck; follow-suit *not* required). Depth from timing the high Ace/Three, counting points, and freedom to discard or trump at will. A 2026 arXiv Monte-Carlo study found strategy effect substantially exceeds the trump-luck advantage. https://www.pagat.com/aceten/briscola.html
- **Gin Rummy** — Native 2p; draw/discard to form melds, knock at ≤10 deadwood. Depth from discard signaling/concealment, combos, and the knock-vs-gin / undercut risk. Luck equalizes over a match. https://en.wikipedia.org/wiki/Gin_rummy
- **Klaberjass (Clobyosh/Bela)** — Native 2p, 32-card pack, 9 each; Jack/9 of trumps top-ranked; melds + Bela (K+Q trump). Strong information-management game; slightly more rules to digest. https://www.pagat.com/jass/bela.html
- **Scopa (2p)** — Native, 40-card deck; capture by matching sums; score most cards/coins, the 7 of coins, and primiera. Card counting (sevens/coins) and sweep-denial; its 4p cousin Scopone is the deeper form. https://www.pagat.com/fishing/scopa.html
- **Durak (2p)** — 36-card deck, attack/defend, last with cards loses. Depth from trump conservation and surrender-vs-defend judgment. *Flag:* weaker at strict 2p — limited hidden info makes luck more prominent. https://gathertogethergames.com/durak

## Honorable mentions / lower depth-to-rules

- **Écarté** — 32-card, 5 each; the propose/discard gamble is neat but the game is short and luck-heavy. https://en.wikipedia.org/wiki/%C3%89cart%C3%A9
- **All Fours / Seven Up** — 52-card; the "beg" decision plus tracking the Jack of trumps adds skill, but heavy luck. https://www.pagat.com/allfours/allfours.html
- **Truc / Put** — Stripped 40/52; minimal rules, pure bluffing/betting on tiny hands; deep psychologically but thin tactically. https://playingcarddecks.com/blogs/all-in/the-very-best-two-player-card-games
- **Bezique** — Two decks (64); melding + brisques; rich but rules-heavy bookkeeping dilutes "deceptively simple." https://www.pagat.com/marriage/bezique.html

## Synthesis

By depth-to-rules ratio, the elite tier is **Goofspiel** (trivial rules, pure game
theory, Nash-solved 2012) and **Schnapsen** (tiny deck, but the closing decision plus
deduction yields enormous depth; analyzed by Tompa, tournament-played). Right behind:
**German Whist** (counting/tempo from almost no rules) and **Cribbage** (two clean
skill layers, statistically studied, competitively played). The next band — **Piquet,
Briscola, Gin Rummy, Klaberjass** — are all strongly skill-dominated and time-tested,
with Briscola now having published Monte-Carlo evidence that strategy outweighs luck.
**Scopa** and **Durak** are easy and fun but lean more on luck at strict 2p.
Mathematically/competitively validated standouts: Goofspiel, Cribbage, Schnapsen, Briscola.
