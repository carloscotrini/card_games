"""Simulated Dodeca players, from naive to card-counting.

Each player implements:
  - choose_card(view) -> a card from view.my_hand
  - want_push(view, my_card) -> bool        (declare a push before the flip)
  - respond_to_push(view, my_card) -> 'accept' | 'fold'

A 'View' (see dodeca.py) exposes only legal information: own hand, both scores, the
face-up discard pile, stock size, and the win target. Players never see the opponent's
current card (moves are simultaneous), which is the whole point.
"""
from __future__ import annotations

import random

from dodeca import ALL_CARDS_SET, resolve


def _unknown(view) -> list:
    """Cards the player cannot account for: not in hand, not in the discard pile.
    This set is the opponent's hand plus the stock — the counting bots model the
    opponent's card as a uniform draw from it (a standard imperfect-info proxy)."""
    seen = set(view.my_hand) | set(view.discard)
    return [c for c in ALL_CARDS_SET if c not in seen]


def _winprob(card, unknown) -> float:
    """P(card beats a uniformly random unknown card). Ties count as non-wins."""
    if not unknown:
        return 0.5
    wins = sum(1 for o in unknown if resolve(card, o) > 0)
    return wins / len(unknown)


class Player:
    """Base: random card, never push, always accept a push."""
    name = "base"

    def __init__(self, rng: random.Random):
        self.rng = rng

    def choose_card(self, view):
        return self.rng.choice(view.my_hand)

    def want_push(self, view, my_card):
        return False

    def respond_to_push(self, view, my_card):
        return "accept"


class RandomBot(Player):
    name = "Random"


class HighCardBot(Player):
    """Naive 'high card wins' play: always dump the highest rank, ignore the ring."""
    name = "HighCard"

    def choose_card(self, view):
        return max(view.my_hand, key=lambda c: c[0])

    def respond_to_push(self, view, my_card):
        return "accept" if my_card[0] >= 11 else "fold"


class OneSuitBot(Player):
    """Degenerate 'hoard one suit' line: commit to the suit it holds most of, playing
    its lowest card of that suit; otherwise throw the lowest card overall."""
    name = "OneSuit"

    def choose_card(self, view):
        counts = {}
        for _, s in view.my_hand:
            counts[s] = counts.get(s, 0) + 1
        target = max(counts, key=lambda s: counts[s])
        in_suit = [c for c in view.my_hand if c[1] == target]
        if in_suit:
            return min(in_suit, key=lambda c: c[0])
        return min(view.my_hand, key=lambda c: c[0])


class CounterBot(Player):
    """Counts the discard pile, models the opponent's card as uniform over unknown
    cards, and plays to win cheaply: win comfortable rounds with the weakest card that
    still wins, and on unwinnable rounds throw the weakest card to conserve strength.
    Never pushes."""
    name = "Counter"
    comfortable = 0.55

    def _scores(self, view):
        unknown = _unknown(view)
        return {c: _winprob(c, unknown) for c in view.my_hand}

    def choose_card(self, view):
        pw = self._scores(view)
        best = max(pw.values())
        if best < 0.5:
            # likely lose regardless -> sacrifice the weakest card, save strong ones
            return min(view.my_hand, key=lambda c: pw[c])
        good = [c for c in view.my_hand if pw[c] >= self.comfortable]
        if good:
            return min(good, key=lambda c: pw[c])  # cheapest comfortable win
        return max(view.my_hand, key=lambda c: pw[c])


class MaxProbBot(CounterBot):
    """Counts cards but does NOT conserve: always plays the card with the highest
    win-probability this round. Separates the value of *counting* from the value of
    *conserving* (CounterBot does both). Never pushes."""
    name = "MaxProb"

    def choose_card(self, view):
        pw = self._scores(view)
        return max(view.my_hand, key=lambda c: pw[c])


class CounterPushBot(CounterBot):
    """CounterBot plus an honest push: push when very confident; accept a push only
    when the committed card is a favourite, else fold to cap the loss at 1."""
    name = "CounterPush"
    push_threshold = 0.72

    def want_push(self, view, my_card):
        return _winprob(my_card, _unknown(view)) >= self.push_threshold

    def respond_to_push(self, view, my_card):
        return "accept" if _winprob(my_card, _unknown(view)) >= 0.5 else "fold"


class BluffPushBot(CounterPushBot):
    """CounterPush that also bluff-pushes weak cards a fraction of the time, and catches
    bluffs by sometimes accepting with a losing card. Tests whether the push supports a
    real yomi layer rather than collapsing to 'push only when strong'."""
    name = "BluffPush"
    bluff_rate = 0.20
    catch_rate = 0.30

    def want_push(self, view, my_card):
        wp = _winprob(my_card, _unknown(view))
        if wp >= self.push_threshold:
            return True
        if wp <= 0.35:  # represent a weak card as a bluff candidate
            return self.rng.random() < self.bluff_rate
        return False

    def respond_to_push(self, view, my_card):
        wp = _winprob(my_card, _unknown(view))
        if wp >= 0.5:
            return "accept"
        # losing card: usually fold, but sometimes accept to punish a bluffer
        return "accept" if self.rng.random() < self.catch_rate else "fold"


ROSTER = [RandomBot, HighCardBot, OneSuitBot, CounterBot, MaxProbBot,
          CounterPushBot, BluffPushBot]
