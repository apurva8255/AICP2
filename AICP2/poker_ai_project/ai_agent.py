# ai_agent.py

from hand_evaluator import evaluate_hand


class AIAgent:

    def __init__(self, name: str):
        self.name = name

    def choose_action(self, game_state, player) -> tuple:
        call_amount = self._get_call_amount(game_state, player)
        hand_strength = self._estimate_hand_strength(game_state, player)

        # strong hand → raise
        if hand_strength >= 4:
            raise_amount = call_amount + self._raise_size(game_state)
            raise_amount = min(raise_amount, player.chips)
            return ("raise", raise_amount)

        # medium hand → call or check
        if hand_strength >= 1:
            if call_amount == 0:
                return ("check", 0)
            if call_amount <= player.chips:
                return ("call", call_amount)
            return ("fold", 0)

        # weak hand → check if free, otherwise fold
        if call_amount == 0:
            return ("check", 0)
        return ("fold", 0)

    def _estimate_hand_strength(self, game_state, player) -> int:
        cards = player.hand + game_state.community_cards
        if len(cards) < 5:
            return self._preflop_strength(player)
        result = evaluate_hand(cards)
        return result[0]

    def _preflop_strength(self, player) -> int:
        if len(player.hand) < 2:
            return 0
        c1, c2 = player.hand
        # pocket pair
        if c1.rank_value == c2.rank_value:
            return 3 if c1.rank_value >= 10 else 1
        # high cards
        high = max(c1.rank_value, c2.rank_value)
        if high >= 13:
            return 2
        if high >= 10:
            return 1
        return 0

    def _get_call_amount(self, game_state, player) -> int:
        max_bet = max(p.current_bet for p in game_state.players)
        return max_bet - player.current_bet

    def _raise_size(self, game_state) -> int:
        return max(20, game_state.pot // 2)

    def __repr__(self) -> str:
        return f'AIAgent("{self.name}")'
