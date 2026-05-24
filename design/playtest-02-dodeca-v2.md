# Playtest 02 — Dodeca v0.2 (lead/response)

**What we tested.** [Playtest 01](playtest-01-dodeca.md) found v0.1's depth was real but
locked behind hidden, simultaneous information, and recommended making moves *sequential*
within a round. [Dodeca v0.2](dodeca-v2-rules.md) does exactly that: a **leader** plays a
card face-up, the **responder** sees it and replies from their own hidden hand; the lead
**alternates** each round; everything else (deck, ring, scoring, race to 7) is unchanged.

**Harness.** `sim/dodeca_v2.py` (engine + role-aware bots) and `sim/simulate_v2.py`
(tests), 800 matches per pairing per seat, seed 20260524. Bots:
`NaiveV2` (play your highest card in both roles — the v0.1 HighCard analog),
`SmartRespV2` (leads naively but *responds* with the cheapest winning counter),
`SmartV2` (counts cards, *leads* the hardest-to-counter card, responds with the cheapest
counter), and `RandomV2`.

---

## Headline: the fix works — and over-corrects

Making the round sequential **unlocks the latent depth**: skill, which barely mattered in
v0.1, now utterly dominates. **But the suit-ring is so strong that the responder almost
always holds a counter, so acting second becomes an overwhelming advantage and the
leader's turn is nearly hopeless.** v0.2 trades v0.1's "too shallow" for "too lopsided."

| Comparison | v0.1 | v0.2 | Change |
|---|---|---|---|
| Skill vs naive aggression | 52.1% (MaxProb v HighCard) | **98.6%** (SmartV2 v NaiveV2) | depth unlocked |
| Skill vs random | 62.4% (Counter v Random) | **99.7%** (SmartV2 v RandomV2) | skill now decisive |
| Smart *responding* alone vs naive | — | **98.3%** | almost all the gain is from reacting to the led card |

So Playtest 01's central recommendation is **validated**: the depth was genuinely there,
and information access was the bottleneck. A player who uses the led card wins ~98% of
the time against one who ignores it.

---

## The new problem: a runaway second-mover advantage

| Measure | Result | Reading |
|---|---|---|
| Responder's share of decided rounds (skilled mirror) | **87.1%** | acting second almost always wins |
| Responder's share (naive mirror) | 50.1% | only because NaiveV2 ignores the led card |
| Responder holds a counter to a high lead (exact, known hands) | **89.5%** | the ring guarantees a counter |
| Leader's best-case round value *even knowing the opp's hand* | **−0.684** | leading is a structural loss, not a play mistake |
| Naive-lead value vs a best response | −0.808 | leading your highest card is punished hardest |

**Why it happens — and why hiding information won't fix it.** The ring ignores rank: the
suit that beats the led suit beats *every* card of it. So a responder only needs to hold
one card of the ring-superior suit to win for certain — and in a six-card hand that
happens ~90% of the time. Crucially, this means **revealing only the led card's *suit*
(not its rank) would not help** — the suit alone is all the responder needs to deploy the
ring counter. The lopsidedness is baked into the ring's rank-independence, not into how
much of the card we show.

**What stays healthy.** Alternating the lead keeps the *match* fair — mirror matches are
~49–50% for seat 0, so there is still no seat advantage. Endings remain decisive. The
problem is purely *within* the round: each player's lead turn is close to a forced loss,
so roughly half of every game is low-agency.

---

## Verdict against the design checklist

- **Skill expression (✓✓).** Enormous — and this is the real win. v0.1's thin skill
  margin (#5, #9) is gone; a thinking player crushes a naive one.
- **Intransitivity now bites (✓).** The ring's rock-paper-scissors finally matters in
  actual play (checklist #7), because the responder can aim a counter.
- **Fair at the match level (✓).** Equilibrium-style symmetry holds via alternating
  leads; ~50% mirror win-rates.
- **Lead/response balance (✗ — the new flaw).** Acting second is worth ~87% of decided
  rounds; the leader has little agency. This is the v0.3 problem to solve.

## Recommendations for v0.3 (rebalance, don't retreat)

Keep the sequential reveal — it is what unlocked the depth — but fix the asymmetry. In
rough order of promise:

1. **Restore rank relevance to the ring (most direct).** Make the ring-superior suit win
   only at *equal-or-higher rank* (so a low counter can't kill a high lead), or have the
   ring only break what would otherwise be a tie. Either change attacks the 89.5%
   guaranteed-counter rate head-on and makes a strong led card genuinely strong.
2. **Make the lead a contested tempo resource.** Switch from fixed alternation to
   **winner-leads** (or loser-leads): if responding is the advantage, then winning a trick
   hands the lead — and thus the disadvantage — to you next round, creating a
   sacrifice/tempo layer the bots don't yet exploit but humans would.
3. **Reward the lead.** Give the leader a bonus (e.g. +1 extra if their lead is *not*
   countered), or let only the responder double (a one-sided push), to price the
   second-mover edge back toward even.

Re-run `simulate_v2.py` after any v0.3 change; the target is to pull the responder's
share of decided rounds from ~87% back toward ~55–65% **while keeping** skill-vs-naive
high (i.e. don't re-lock the depth).

## Honest limitations

- The "smart" bots respond near-optimally but do **no tempo/sacrifice reasoning** and the
  leader bot is a simple "fewest-beaters" heuristic; a human (or a CFR learner) would play
  the lead better than −0.68, so the *real* lead penalty is somewhat smaller than the bots
  suggest — but the structural 89.5% counter rate is exact and not bot-dependent.
- The push is omitted in v0.2; reintroducing a one-sided push is itself a v0.3 lever (#3).
- Numbers reproduce from [`sim/`](sim/CLAUDE.md): `python3 simulate_v2.py --matches 800`;
  raw output saved as `sim/v2_results.json` / `sim/v2_last_run.txt`.
