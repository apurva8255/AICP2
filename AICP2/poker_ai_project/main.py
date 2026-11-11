# main.py

import pygame
import sys
from game_state import GameState
from ai_agent import AIAgent
from hand_evaluator import evaluate_hand
from ui import (
    init_screen, draw_table, draw_action_buttons,
    get_player_action, SCREEN_WIDTH
)


FPS = 30
SMALL_BLIND = 10
BIG_BLIND = 20


def apply_action(game_state, player, action, amount):
    if action == "fold":
        player.fold()
    elif action == "check":
        pass
    elif action == "call":
        amount = min(amount, player.chips)
        player.bet(amount)
        game_state.add_to_pot(amount)
    elif action == "raise":
        amount = min(amount, player.chips)
        player.bet(amount)
        game_state.add_to_pot(amount)


def post_blinds(game_state):
    sb_index = (game_state.dealer_index + 1) % len(game_state.players)
    bb_index = (game_state.dealer_index + 2) % len(game_state.players)

    sb_player = game_state.players[sb_index]
    bb_player = game_state.players[bb_index]

    sb = min(SMALL_BLIND, sb_player.chips)
    bb = min(BIG_BLIND, bb_player.chips)

    sb_player.bet(sb)
    game_state.add_to_pot(sb)

    bb_player.bet(bb)
    game_state.add_to_pot(bb)


def do_showdown(game_state):
    active = game_state.active_players()
    if len(active) == 1:
        winner = active[0]
        winner.chips += game_state.pot
        return f"{winner.name} wins {game_state.pot} (opponent folded)"

    best_hands = []
    for player in active:
        cards = player.hand + game_state.community_cards
        score = evaluate_hand(cards)
        best_hands.append((score, player))

    best_hands.sort(key=lambda x: x[0], reverse=True)
    winner = best_hands[0][1]
    winner.chips += game_state.pot
    return f"{winner.name} wins {game_state.pot}"


def start_new_hand(game_state):
    game_state.reset_for_new_hand()
    post_blinds(game_state)
    game_state.deal_hole_cards()


def main():
    screen = init_screen()
    clock = pygame.time.Clock()

    game_state = GameState(["Player", "AI"])
    ai = AIAgent("AI")

    human = game_state.players[0]
    ai_player = game_state.players[1]

    start_new_hand(game_state)

    turn = 0  # 0 = human, 1 = AI
    message = ""
    message_timer = 0
    waiting_for_input = True

    font = pygame.font.SysFont("segoeui", 22)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and waiting_for_input:
                if turn == 0 and game_state.betting_round != "showdown":
                    call_amount = max(p.current_bet for p in game_state.players) - human.current_bet
                    raise_amount = call_amount + max(20, game_state.pot // 2)
                    raise_amount = min(raise_amount, human.chips)

                    result = get_player_action(event.pos, call_amount, raise_amount)
                    if result:
                        action, amount = result
                        apply_action(game_state, human, action, amount)
                        turn = 1
                        waiting_for_input = False

        # AI turn
        if not waiting_for_input and turn == 1 and game_state.betting_round != "showdown":
            if not ai_player.folded:
                action, amount = ai.choose_action(game_state, ai_player)
                apply_action(game_state, ai_player, action, amount)
                message = f"AI: {action} {amount}"
                message_timer = FPS * 2

            # advance round after both players act
            if len(game_state.active_players()) < 2:
                game_state.betting_round = "showdown"
            else:
                game_state.advance_round()

            turn = 0
            waiting_for_input = True

        # showdown
        if game_state.betting_round == "showdown":
            result = do_showdown(game_state)
            message = result
            message_timer = FPS * 3

            game_state.betting_round = "done"

        # auto restart after showing result
        if game_state.betting_round == "done" and message_timer <= 0:
            start_new_hand(game_state)
            turn = 0
            waiting_for_input = True

        # render
        draw_table(screen, game_state)
        draw_action_buttons(screen)

        if message and message_timer > 0:
            msg_surface = font.render(message, True, (255, 255, 255))
            screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 400))
            message_timer -= 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
