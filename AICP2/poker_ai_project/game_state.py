# game_state.py

from deck import Deck
from player import Player


ROUND_ORDER = ["preflop", "flop", "turn", "river", "showdown"]


class GameState:

    def __init__(self, player_names: list[str], starting_chips: int = 1000):
        self.deck = Deck()
        self.players = [Player(name, starting_chips) for name in player_names]
        self.community_cards = []
        self.pot = 0
        self.dealer_index = 0
        self.current_player_index = 0
        self.betting_round = "preflop"

    def deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.receive_card(card)

    def deal_flop(self):
        for _ in range(3):
            card = self.deck.draw_card()
            if card:
                self.community_cards.append(card)

    def deal_turn(self):
        card = self.deck.draw_card()
        if card:
            self.community_cards.append(card)

    def deal_river(self):
        card = self.deck.draw_card()
        if card:
            self.community_cards.append(card)

    def add_to_pot(self, amount: int):
        self.pot += amount

    def reset_bets(self):
        for player in self.players:
            player.current_bet = 0

    def advance_round(self):
        current_index = ROUND_ORDER.index(self.betting_round)
        if current_index < len(ROUND_ORDER) - 1:
            self.betting_round = ROUND_ORDER[current_index + 1]
            self.reset_bets()

            if self.betting_round == "flop":
                self.deal_flop()
            elif self.betting_round == "turn":
                self.deal_turn()
            elif self.betting_round == "river":
                self.deal_river()

    def active_players(self):
        return [p for p in self.players if not p.folded]

    def reset_for_new_hand(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        self.betting_round = "preflop"
        for player in self.players:
            player.reset_for_round()

    def __repr__(self) -> str:
        cards_str = ", ".join(str(c) for c in self.community_cards)
        return f'GameState(round="{self.betting_round}", pot={self.pot}, community_cards=[{cards_str}])'
