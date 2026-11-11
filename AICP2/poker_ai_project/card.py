# card.py

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']

RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, start=2)}

SUIT_SYMBOLS = {
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    'spades': '♠'
}


class Card:

    def __init__(self, rank: str, suit: str):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.rank = rank
        self.suit = suit

    @property
    def rank_value(self) -> int:
        return RANK_VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank}{SUIT_SYMBOLS[self.suit]}"

    def __repr__(self) -> str:
        return f'Card("{self.rank}", "{self.suit}")'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_value < other.rank_value

    def __le__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_value <= other.rank_value

    def __gt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_value > other.rank_value

    def __ge__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_value >= other.rank_value

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))
