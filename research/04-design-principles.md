# Category 4 — Design principles

Background theory, frameworks, and papers to inform designing our own two-player
standard-deck card game. (Not a survey of existing games.)

## 1. Combinatorial / mathematical game theory

- **Minimax & zero-sum two-player theory (von Neumann, 1928).** In any two-player
  zero-sum game there exists an optimal strategy maximizing your worst-case outcome.
  *Why it matters:* most 2p card games are effectively zero-sum, so you can reason
  about whether a position has a forced best line and whether any line dominates.
  https://en.wikipedia.org/wiki/Combinatorial_game_theory
- **Perfect vs. imperfect information.** Hidden cards mean each player only partially
  observes state; this is why card games resist "solving" and require probabilistic/
  Bayesian reasoning. Algorithms like Information-Set MCTS and counterfactual regret
  were built for this class. *Why it matters:* hidden information is your single most
  powerful lever for depth and bluffing. https://arxiv.org/pdf/2212.12567
- **Game-tree complexity & first-player advantage.** Depth/branching factor determine
  how hard a game is to solve; many turn-based games confer a first-mover edge.
  *Why it matters:* want a branching factor high enough to resist trivial solving, plus
  a mechanism to neutralize first-player advantage.
  https://www.numberanalytics.com/blog/game-trees-combinatorial-game-theory

## 2. Depth vs. complexity (the elegance ratio)

- **Complexity = cost to learn; depth = ability to keep mastering.** A good game is
  high-depth, low-complexity; that ratio is *elegance*. Each mechanic adds depth
  (revenue) and complexity (cost) in differing proportions — favor mechanics cheap to
  explain but rich in emergent possibility. *Why it matters:* a 52-card deck has
  near-zero learning cost, so depth should come from rule *interactions*, not rule count.
  https://www.gamedeveloper.com/design/easy-to-learn-hard-to-master · https://www.accidentalcyclops.com/depth-vs-complexity/
- **Emergent depth.** Depth should emerge from a few simple elements combining —
  "complexity of choice over complexity of action." *Why it matters:* aim for rules
  learnable in minutes whose combinations still surprise veterans.
  https://www.gamedeveloper.com/design/depth-from-complexity-pt-2

## 3. Designer wisdom

- **Reiner Knizia — scoring drives behavior.** The victory/scoring condition is the
  most important element because it dictates player behavior; build simple rules from
  which a "second level of depth" emerges, and abstract away theme. *Why it matters:*
  design the victory condition first. https://en.wikipedia.org/wiki/Reiner_Knizia
- **David Sirlin — degenerate strategies & yomi.** Some games *degenerate* (collapse
  to one dominant tactic) at high skill; good games provide counters, so apparent
  dominant tactics turn out beatable, creating recursive mind-reading ("yomi").
  *Why it matters:* stress-test against a "best abusable line" — if one exists with no
  counter, the game is broken. https://www.sirlin.net/articles/playing-to-win
- **Mark Rosewater — "Twenty Years, Twenty Lessons."** "Restrictions breed creativity";
  design for a target audience, not everyone; "if everyone likes it but no one loves it,
  it will fail." *Why it matters:* embrace the deck's constraints; aim for a game some
  players love. https://magic.wizards.com/en/news/making-magic/twenty-years-twenty-lessons-part-1-2016-05-30

## 4. Balance & fairness mechanisms

- **Pie rule / swap rule.** After P1's first move, P2 may accept it or swap sides,
  incentivizing P1 to make the *fairest possible* opening (used in Hex, TwixT). The
  procedural version of "I cut, you choose." *Why it matters:* the cleanest known fix
  for opening-advantage in a 2p game. https://en.wikipedia.org/wiki/Pie_rule
- **Auctions / bidding & cut-and-choose.** Auctions let players set resource value, so
  balance is enforced by players rather than the designer; divide-and-choose guarantees
  each party at least half by their own valuation. *Why it matters:* a bidding or
  cut-and-choose sub-mechanic offloads balancing and adds a decision.
  http://gamedesignaspect.blogspot.com/2013/12/auctions-as-game-balancing-tool.html
- **Luck/skill coexistence & catch-up.** Elias/Garfield/Gutschera show luck and skill
  aren't opposites — *some* luck is desirable (lets weaker players sometimes win, keeps
  outcomes uncertain); they also formalize "snowball vs. catch-up." *Why it matters:*
  tune the luck/skill dial deliberately and add catch-up pressure so a lead isn't an
  automatic win. https://boardgamesnob.com/2016/07/27/luck-and-skill/

## 5. What makes a decision meaningful

- **Sid Meier — "a series of interesting decisions."** A choice is interesting only
  when no option clearly dominates, options aren't equally attractive, the player can
  make an *informed* choice, and consequences are visible. *Why it matters:* audit every
  turn — if there's an obviously-best play, remove the choice or add a counterbalancing
  cost. https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions
- **Intransitivity & bluffing.** Rock-paper-scissors relationships prevent any single
  strategy from dominating and, with hidden information, enable bluffing and yomi.
  *Why it matters:* intransitive options + hidden hands = built-in mind games.

## 6. Academic papers / automated evaluation

- **Cameron Browne — Ludi / Yavalath (Evolutionary Game Design).** Ludi auto-generates
  and *evaluates* games via measurable criteria (drawishness, decisiveness, depth,
  lead-change, forcing-move tension); Yavalath was the first computer-designed
  commercially published game. *Why it matters:* concrete, computable metrics to apply
  to playtest data. https://link.springer.com/article/10.1007/s10710-012-9165-6
- **Characteristics of Games (Elias, Garfield, Gutschera, MIT Press 2012).** A formal
  vocabulary along axes (players, luck/skill, snowball/catch-up, reward/effort, decision
  complexity). *Why it matters:* the best checklist-style framework to evaluate a
  prototype. https://books.google.com/books/about/Characteristics_of_Games.html?id=QVP8AQAAQBAJ

## Design checklist

Concrete principles to apply when inventing our two-player standard-deck game:

1. **Define the scoring/victory condition first** (Knizia) — simple to state, clearly drives behavior.
2. **Exploit the deck's zero learning cost** — rules teachable in under ~5 minutes; depth from *interactions*, not rule count.
3. **Use hidden information deliberately** (hidden hand / face-down cards) as the primary engine of depth, bluffing, and yomi.
4. **Neutralize first-player advantage** — pie/swap rule, an opening bid, or cut-and-choose for the deal.
5. **Audit every turn for dominant strategies** — if one option is always best, add a cost, hidden info, or an intransitive counter.
6. **Build at least one explicit trade-off / tension axis** (e.g., score now vs. set up later; reveal vs. conceal) so choices have visible consequences.
7. **Add an intransitive (RPS-style) relationship** among options or card roles to prevent single-strategy dominance and enable mind games.
8. **Tune the luck/skill dial intentionally** — keep some chance (shuffle/draw) so weaker players occasionally win, but ensure skill dominates over a match.
9. **Include a catch-up / anti-snowball mechanic** so an early lead isn't a guaranteed win.
10. **Include a "knock/close" or commitment decision** — a tension point where a player locks in or pushes, trading safety for reward (cf. Schnapsen's closing, Gin's knock).
11. **Stress-test the "best abusable line"** in playtesting; confirm every strong tactic has a counter (degeneracy check).
12. **Evaluate against measurable quality metrics** (Browne/Ludi): low draw rate, frequent lead changes, decisive endings, forcing moves, and a branching factor high enough to resist trivial solving.

### Key sources
- CGT / imperfect info: https://en.wikipedia.org/wiki/Combinatorial_game_theory · https://arxiv.org/pdf/2212.12567
- Depth vs complexity: https://www.gamedeveloper.com/design/easy-to-learn-hard-to-master · https://www.accidentalcyclops.com/depth-vs-complexity/
- Designers: https://www.sirlin.net/articles/playing-to-win · https://en.wikipedia.org/wiki/Reiner_Knizia · https://magic.wizards.com/en/news/making-magic/twenty-years-twenty-lessons-part-1-2016-05-30
- Balance: https://en.wikipedia.org/wiki/Pie_rule · http://gamedesignaspect.blogspot.com/2013/12/auctions-as-game-balancing-tool.html · https://boardgamesnob.com/2016/07/27/luck-and-skill/
- Meaningful decisions: https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions
- Academic: https://link.springer.com/article/10.1007/s10710-012-9165-6 · https://books.google.com/books/about/Characteristics_of_Games.html?id=QVP8AQAAQBAJ

> Note: a few primary pages (Sirlin, Game Developer, Accidental Cyclops) returned HTTP
> 403 to the research fetch tool; those summaries draw on search excerpts plus the
> canonical URLs above, which are accessible in a browser.
