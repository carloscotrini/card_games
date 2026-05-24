"""Dodeca v0.2 engine + bots: the LEAD / RESPONSE variant.

Playtest 01 found that v0.1's depth is real but locked behind hidden, simultaneous
information: you can only exploit the suit-ring when you know the opponent's suit, and
simultaneous hidden play hides exactly that. v0.2 tests the recommended fix: make moves
*sequential* within a round.

  Each round one player LEADS a card face-up; the other RESPONDS, seeing the led card,
  from their own (still hidden) hand. The lead alternates every round. Resolution
  (suit-ring, then rank) and scoring are identical to v0.1. The push is dropped for now
  to isolate the information change.

This re-uses resolve()/is_ring_matchup()/the deck from the v0.1 engine; only the
turn structure changes. Bots implement lead(view) and respond(view, led_card).
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from dodeca import (ALL_CARDS, ALL_CARDS_SET, HAND_SIZE, View, is_ring_matchup,
                    resolve)


# --------------------------------------------------------------------------- #
# Shared counting helpers (mirror players.py so the bots are comparable).      #
# --------------------------------------------------------------------------- #
def unknown_cards(view) -> list:
    seen = set(view.my_hand) | set(view.discard)
    return [c for c in ALL_CARDS_SET if c not in seen]


def n_beaters(card, pool) -> int:
    """How many cards in `pool` would beat `card` if played against it."""
    return sum(1 for o in pool if resolve(o, card) > 0)


def cheapest_winning_response(hand, led):
    """Lowest-rank card that beats `led`; None if the hand cannot beat it."""
    winners = [c for c in hand if resolve(c, led) > 0]
    if not winners:
        return None
    return min(winners, key=lambda c: c[0])


# --------------------------------------------------------------------------- #
# Bots. Each defines lead(view) and respond(view, led).                        #
# --------------------------------------------------------------------------- #
class V2Player:
    name = "base"

    def __init__(self, rng: random.Random):
        self.rng = rng

    def lead(self, view):
        return self.rng.choice(view.my_hand)

    def respond(self, view, led):
        return self.rng.choice(view.my_hand)


class RandomV2(V2Player):
    name = "RandomV2"


class NaiveV2(V2Player):
    """'Play high' in both roles, ignoring the led card -- the v0.1 HighCard analog."""
    name = "NaiveV2"

    def lead(self, view):
        return max(view.my_hand, key=lambda c: c[0])

    def respond(self, view, led):
        return max(view.my_hand, key=lambda c: c[0])


class SmartRespV2(V2Player):
    """Leads naively (highest rank) but RESPONDS well: counter the led card with the
    cheapest winning card, else dump the weakest. Isolates the value of using the led
    information when responding."""
    name = "SmartRespV2"

    def lead(self, view):
        return max(view.my_hand, key=lambda c: c[0])

    def respond(self, view, led):
        c = cheapest_winning_response(view.my_hand, led)
        return c if c is not None else min(view.my_hand, key=lambda c: c[0])


class SmartV2(SmartRespV2):
    """Full skill: counts cards and LEADS the hardest-to-counter card (fewest beaters
    among the unseen cards), and responds with the cheapest winning counter."""
    name = "SmartV2"

    def lead(self, view):
        pool = unknown_cards(view)
        # fewest cards that could beat it; break ties toward higher rank (also wins
        # rank/neutral contests if uncountered).
        return min(view.my_hand, key=lambda c: (n_beaters(c, pool), -c[0]))


ROSTER_V2 = [RandomV2, NaiveV2, SmartRespV2, SmartV2]


# --------------------------------------------------------------------------- #
# Engine.                                                                      #
# --------------------------------------------------------------------------- #
@dataclass
class MatchStatsV2:
    winner: Optional[int] = None
    score: tuple = (0, 0)
    rounds: int = 0
    ties: int = 0
    ring_decided: int = 0
    rank_decided: int = 0
    lead_changes: int = 0
    comeback: bool = False
    ended_by_target: bool = False
    leader_round_wins: int = 0     # decided rounds won by the round's leader
    responder_round_wins: int = 0  # decided rounds won by the responder


def play_match_v2(p0, p1, rng: random.Random, *, win_target: int = 7,
                  neutral_mode: str = "rank", start_leader: int = 0) -> MatchStatsV2:
    players = [p0, p1]
    deck = list(ALL_CARDS)
    rng.shuffle(deck)
    hands = [deck[0:HAND_SIZE], deck[HAND_SIZE:2 * HAND_SIZE]]
    stock = deck[2 * HAND_SIZE:]
    discard: list = []
    scores = [0, 0]
    st = MatchStatsV2()
    prev_sign = 0
    score_path = []
    leader = start_leader

    def view(i: int) -> View:
        return View(my_hand=list(hands[i]), my_score=scores[i], opp_score=scores[1 - i],
                    discard=list(discard), stock_count=len(stock), win_target=win_target,
                    my_index=i)

    safety = 0
    while max(scores) < win_target and (hands[0] or hands[1]):
        safety += 1
        if safety > 200:
            break
        st.rounds += 1
        responder = 1 - leader

        led = players[leader].lead(view(leader))
        hands[leader].remove(led)
        resp = players[responder].respond(view(responder), led)
        hands[responder].remove(resp)

        # resolve() is from the leader's perspective if we pass (led, resp)
        r = resolve(led, resp)
        round_winner = None
        if r == 0 or (neutral_mode == "replay" and not is_ring_matchup(led, resp)
                      and led[1] != resp[1]):
            if r == 0:
                st.ties += 1
        else:
            leader_won = r > 0
            round_winner = leader if leader_won else responder
            if is_ring_matchup(led, resp):
                st.ring_decided += 1
            else:
                st.rank_decided += 1
            if leader_won:
                st.leader_round_wins += 1
            else:
                st.responder_round_wins += 1
            scores[round_winner] += 1

        discard.append(led)
        discard.append(resp)
        # refill: leader first
        for i in (leader, responder):
            if len(hands[i]) < HAND_SIZE and stock:
                hands[i].append(stock.pop())

        diff = scores[0] - scores[1]
        sign = (diff > 0) - (diff < 0)
        if sign != 0 and prev_sign != 0 and sign != prev_sign:
            st.lead_changes += 1
        if sign != 0:
            prev_sign = sign
        score_path.append((scores[0], scores[1]))
        leader = 1 - leader  # alternate the lead

    st.score = (scores[0], scores[1])
    st.winner = None if scores[0] == scores[1] else (0 if scores[0] > scores[1] else 1)
    st.ended_by_target = max(scores) >= win_target
    if st.winner is not None:
        w = st.winner
        max_def = max((b - a if w == 0 else a - b) for a, b in score_path) if score_path else 0
        st.comeback = max_def >= 2
    return st
