# player.py


class Player:

    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def receive_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def bet(self, amount: int):
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True

    def reset_for_round(self):
        self.clear_hand()
        self.current_bet = 0
        self.folded = False

    def __repr__(self) -> str:
        return f'Player("{self.name}", chips={self.chips}, cards={len(self.hand)})'
