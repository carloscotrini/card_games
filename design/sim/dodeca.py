"""Dodeca game engine (v0.1 rules).

Implements the rules in design/dodeca-rules.md. The engine is parameterised so the
tuning dials (win target, neutral-suit handling) can be swept by the simulator.

Card = (rank, suit). rank is an int 2..14 (J=11, Q=12, K=13, A=14). suit in 'CDHS'.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

SUITS = "CDHS"
RANKS = list(range(2, 15))  # 2..14, Ace high
ALL_CARDS = [(r, s) for s in SUITS for r in RANKS]
ALL_CARDS_SET = frozenset(ALL_CARDS)
HAND_SIZE = 6

# Suit ring: each suit beats the next; Spades wraps to beat Clubs (C->D->H->S->C).
RING_BEATS = {"C": "D", "D": "H", "H": "S", "S": "C"}


def resolve(a: tuple, b: tuple) -> int:
    """Compare two flipped cards. Return +1 if a wins, -1 if b wins, 0 on a tie.

    Rules:
      - same suit  -> higher rank wins (no tie possible, single deck)
      - adjacent suits in the ring -> the ring decides, rank ignored
      - neutral (opposite) suits -> higher rank wins; equal rank is a tie
    """
    ra, sa = a
    rb, sb = b
    if sa == sb:
        return 1 if ra > rb else -1
    if RING_BEATS[sa] == sb:
        return 1
    if RING_BEATS[sb] == sa:
        return -1
    # neutral pair -> rank decides
    if ra > rb:
        return 1
    if rb > ra:
        return -1
    return 0


def is_ring_matchup(a: tuple, b: tuple) -> bool:
    sa, sb = a[1], b[1]
    return RING_BEATS[sa] == sb or RING_BEATS[sb] == sa


@dataclass
class View:
    """What a player is allowed to see when deciding."""
    my_hand: list
    my_score: int
    opp_score: int
    discard: list
    stock_count: int
    win_target: int
    my_index: int


@dataclass
class MatchStats:
    winner: Optional[int] = None  # 0, 1, or None for a draw
    score: tuple = (0, 0)
    rounds: int = 0
    lead_changes: int = 0
    ring_decided: int = 0
    rank_decided: int = 0
    ties: int = 0
    pushes: int = 0
    push_folds: int = 0
    push_accepts: int = 0
    pusher_won_points: int = 0
    winner_max_deficit: int = 0  # biggest margin the eventual winner trailed by
    comeback: bool = False       # winner trailed by >= 2 at some point
    ended_by_target: bool = False


def play_match(p0, p1, rng: random.Random, *, win_target: int = 7,
               neutral_mode: str = "rank") -> MatchStats:
    """Play one match to win_target points. neutral_mode in {'rank','replay'}.

    neutral_mode='replay' makes neutral-suit pairs a no-score replay instead of a
    rank contest (a tuning dial from the rules).
    """
    players = [p0, p1]
    deck = list(ALL_CARDS)
    rng.shuffle(deck)
    hands = [deck[0:HAND_SIZE], deck[HAND_SIZE:2 * HAND_SIZE]]
    stock = deck[2 * HAND_SIZE:]
    discard: list = []
    scores = [0, 0]

    st = MatchStats()
    prev_sign = 0

    def view(i: int) -> View:
        return View(my_hand=list(hands[i]), my_score=scores[i], opp_score=scores[1 - i],
                    discard=list(discard), stock_count=len(stock), win_target=win_target,
                    my_index=i)

    def refill(first: int):
        order = [first, 1 - first]
        for i in order:
            if len(hands[i]) < HAND_SIZE and stock:
                hands[i].append(stock.pop())

    def award(winner_idx: int, pts: int):
        scores[winner_idx] += pts
        if winner_idx == 0:
            st.pusher_won_points  # no-op placeholder
        # track winner deficit later via running record

    # Track running deficit for whoever eventually wins; we record the score path.
    score_path = []

    safety = 0
    while max(scores) < win_target and (hands[0] or hands[1]):
        safety += 1
        if safety > 200:
            break
        st.rounds += 1

        # 1. Both commit a card (each chooses from own hand).
        c0 = players[0].choose_card(view(0))
        c1 = players[1].choose_card(view(1))
        hands[0].remove(c0)
        hands[1].remove(c1)
        committed = [c0, c1]

        # 2. Push phase: poll intentions on own committed card.
        wants = [players[0].want_push(view(0), c0), players[1].want_push(view(1), c1)]
        pusher = None
        if wants[0] and wants[1]:
            pusher = rng.randint(0, 1)  # only one push per round
        elif wants[0]:
            pusher = 0
        elif wants[1]:
            pusher = 1

        round_winner = None
        pts = 1
        resolved = True

        if pusher is not None:
            st.pushes += 1
            opp = 1 - pusher
            resp = players[opp].respond_to_push(view(opp), committed[opp])
            if resp == "fold":
                st.push_folds += 1
                round_winner = pusher
                pts = 1
                resolved = False  # conceded without a flip
            else:
                st.push_accepts += 1
                pts = 2  # accepted -> doubled

        if resolved:
            r = resolve(c0, c1)
            if r == 0 or (neutral_mode == "replay" and not is_ring_matchup(c0, c1)
                          and c0[1] != c1[1]):
                # tie, or neutral-as-replay: no score this round
                if r == 0:
                    st.ties += 1
                round_winner = None
            else:
                round_winner = 0 if r > 0 else 1
                if is_ring_matchup(c0, c1):
                    st.ring_decided += 1
                else:
                    st.rank_decided += 1

        if round_winner is not None:
            scores[round_winner] += pts
            if pusher is not None and round_winner == pusher:
                st.pusher_won_points += 1

        # 3. Discard both committed cards (face-up count) and refill.
        discard.append(c0)
        discard.append(c1)
        first = round_winner if round_winner is not None else (pusher if pusher is not None else 0)
        refill(first)

        # lead-change tracking
        diff = scores[0] - scores[1]
        sign = (diff > 0) - (diff < 0)
        if sign != 0 and prev_sign != 0 and sign != prev_sign:
            st.lead_changes += 1
        if sign != 0:
            prev_sign = sign
        score_path.append((scores[0], scores[1]))

    # Resolve match result.
    if scores[0] == scores[1]:
        st.winner = None
    else:
        st.winner = 0 if scores[0] > scores[1] else 1
    st.score = (scores[0], scores[1])
    st.ended_by_target = max(scores) >= win_target

    # winner deficit / comeback from the score path
    if st.winner is not None:
        w = st.winner
        max_def = 0
        for a, b in score_path:
            mine, theirs = (a, b) if w == 0 else (b, a)
            max_def = max(max_def, theirs - mine)
        st.winner_max_deficit = max_def
        st.comeback = max_def >= 2

    return st
