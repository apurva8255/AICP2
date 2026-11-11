# hand_evaluator.py

from itertools import combinations
from card import Card


HAND_RANKS = {
    'high_card': 0,
    'pair': 1,
    'two_pair': 2,
    'three_of_a_kind': 3,
    'straight': 4,
    'flush': 5,
    'full_house': 6,
    'four_of_a_kind': 7,
    'straight_flush': 8
}


def _count_ranks(cards):
    counts = {}
    for card in cards:
        counts[card.rank_value] = counts.get(card.rank_value, 0) + 1
    return counts


def _detect_flush(cards):
    suit_groups = {}
    for card in cards:
        suit_groups.setdefault(card.suit, []).append(card)
    for suit, group in suit_groups.items():
        if len(group) >= 5:
            return sorted(group, key=lambda c: c.rank_value, reverse=True)[:5]
    return None


def _detect_straight(cards):
    values = sorted(set(card.rank_value for card in cards), reverse=True)

    # check for ace-low straight (A-2-3-4-5)
    if set([14, 2, 3, 4, 5]).issubset(set(values)):
        return 5

    for i in range(len(values) - 4):
        window = values[i:i + 5]
        if window[0] - window[4] == 4:
            return window[0]

    return None


def _evaluate_five(cards):
    counts = _count_ranks(cards)
    values = sorted(counts.keys(), reverse=True)
    freq = sorted(counts.values(), reverse=True)

    is_flush = len(set(card.suit for card in cards)) == 1
    sorted_values = sorted((card.rank_value for card in cards), reverse=True)

    # straight check
    is_straight = False
    straight_high = None
    unique = sorted(set(sorted_values), reverse=True)
    if len(unique) == 5:
        if unique[0] - unique[4] == 4:
            is_straight = True
            straight_high = unique[0]
        elif unique == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

    # straight flush
    if is_straight and is_flush:
        return (8, [straight_high])

    # four of a kind
    if freq == [4, 1]:
        quad = [v for v, c in counts.items() if c == 4][0]
        kicker = [v for v, c in counts.items() if c == 1][0]
        return (7, [quad, kicker])

    # full house
    if freq == [3, 2]:
        triple = [v for v, c in counts.items() if c == 3][0]
        pair = [v for v, c in counts.items() if c == 2][0]
        return (6, [triple, pair])

    # flush
    if is_flush:
        return (5, sorted_values)

    # straight
    if is_straight:
        return (4, [straight_high])

    # three of a kind
    if freq == [3, 1, 1]:
        triple = [v for v, c in counts.items() if c == 3][0]
        kickers = sorted([v for v, c in counts.items() if c == 1], reverse=True)
        return (3, [triple] + kickers)

    # two pair
    if freq == [2, 2, 1]:
        pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)
        kicker = [v for v, c in counts.items() if c == 1][0]
        return (2, pairs + [kicker])

    # pair
    if freq == [2, 1, 1, 1]:
        pair = [v for v, c in counts.items() if c == 2][0]
        kickers = sorted([v for v, c in counts.items() if c == 1], reverse=True)
        return (1, [pair] + kickers)

    # high card
    return (0, sorted_values)


def evaluate_hand(cards):
    if len(cards) < 5:
        raise ValueError("Need at least 5 cards to evaluate a hand")

    best = None
    for combo in combinations(cards, 5):
        result = _evaluate_five(list(combo))
        if best is None or result > best:
            best = result

    return best
