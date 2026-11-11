# ui.py

import pygame

# screen constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CARD_WIDTH = 60
CARD_HEIGHT = 90

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (200, 30, 30)
GRAY = (180, 180, 180)
LIGHT_GRAY = (220, 220, 220)
BLUE = (50, 100, 200)
GOLD = (255, 215, 0)

# suit symbols
SUIT_SYMBOLS = {
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    'spades': '♠'
}

SUIT_COLORS = {
    'hearts': RED,
    'diamonds': RED,
    'clubs': BLACK,
    'spades': BLACK
}

# button definitions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_Y = 640
BUTTON_GAP = 20
BUTTONS = [
    {"label": "Fold", "action": "fold"},
    {"label": "Check", "action": "check"},
    {"label": "Call", "action": "call"},
    {"label": "Raise", "action": "raise"},
]

# precompute button rects
_total_width = len(BUTTONS) * BUTTON_WIDTH + (len(BUTTONS) - 1) * BUTTON_GAP
_start_x = (SCREEN_WIDTH - _total_width) // 2
BUTTON_RECTS = {}
for i, btn in enumerate(BUTTONS):
    x = _start_x + i * (BUTTON_WIDTH + BUTTON_GAP)
    BUTTON_RECTS[btn["action"]] = pygame.Rect(x, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)


def init_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Texas Hold'em Poker")
    return screen


def _get_font(size=20):
    return pygame.font.SysFont("segoeui", size)


def _draw_card(screen, card, position):
    x, y = position
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, WHITE, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    font = _get_font(16)
    symbol = SUIT_SYMBOLS.get(card.suit, '?')
    color = SUIT_COLORS.get(card.suit, BLACK)

    rank_surface = font.render(card.rank, True, color)
    suit_surface = font.render(symbol, True, color)

    screen.blit(rank_surface, (x + 5, y + 5))
    screen.blit(suit_surface, (x + 5, y + 25))

    big_font = _get_font(22)
    center_surface = big_font.render(symbol, True, color)
    cx = x + CARD_WIDTH // 2 - center_surface.get_width() // 2
    cy = y + CARD_HEIGHT // 2 - center_surface.get_height() // 2 + 5
    screen.blit(center_surface, (cx, cy))


def _draw_card_back(screen, position):
    x, y = position
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, BLUE, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    font = _get_font(18)
    text = font.render("?", True, WHITE)
    tx = x + CARD_WIDTH // 2 - text.get_width() // 2
    ty = y + CARD_HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (tx, ty))


def draw_player_hand(screen, player, position, show_cards=True):
    x, y = position
    for i, card in enumerate(player.hand):
        card_x = x + i * (CARD_WIDTH + 10)
        if show_cards:
            _draw_card(screen, card, (card_x, y))
        else:
            _draw_card_back(screen, (card_x, y))


def draw_community_cards(screen, community_cards):
    start_x = (SCREEN_WIDTH - (5 * CARD_WIDTH + 4 * 10)) // 2
    y = 280
    for i, card in enumerate(community_cards):
        x = start_x + i * (CARD_WIDTH + 10)
        _draw_card(screen, card, (x, y))


def draw_table(screen, game_state):
    screen.fill(DARK_GREEN)

    # table felt
    table_rect = pygame.Rect(80, 100, SCREEN_WIDTH - 160, 480)
    pygame.draw.ellipse(screen, GREEN, table_rect)
    pygame.draw.ellipse(screen, GOLD, table_rect, 3)

    font = _get_font(22)
    small_font = _get_font(16)

    # pot
    pot_text = font.render(f"Pot: {game_state.pot}", True, GOLD)
    screen.blit(pot_text, (SCREEN_WIDTH // 2 - pot_text.get_width() // 2, 240))

    # round
    round_text = small_font.render(f"Round: {game_state.betting_round.upper()}", True, WHITE)
    screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 210))

    # community cards
    draw_community_cards(screen, game_state.community_cards)

    # players
    for i, player in enumerate(game_state.players):
        if i == 0:
            # human player at bottom
            px, py = SCREEN_WIDTH // 2 - 70, 500
            show = True
        else:
            # AI player at top
            px, py = SCREEN_WIDTH // 2 - 70, 110
            show = False

        draw_player_hand(screen, player, (px, py), show_cards=show)

        # name and chips
        info = f"{player.name}  Chips: {player.chips}"
        if player.folded:
            info += "  [FOLDED]"
        info_surface = small_font.render(info, True, WHITE)
        screen.blit(info_surface, (px, py - 25))


def draw_action_buttons(screen):
    font = _get_font(18)
    for btn in BUTTONS:
        rect = BUTTON_RECTS[btn["action"]]
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        label = font.render(btn["label"], True, BLACK)
        lx = rect.x + rect.width // 2 - label.get_width() // 2
        ly = rect.y + rect.height // 2 - label.get_height() // 2
        screen.blit(label, (lx, ly))


def get_player_action(mouse_pos, call_amount=0, raise_amount=0):
    for btn in BUTTONS:
        rect = BUTTON_RECTS[btn["action"]]
        if rect.collidepoint(mouse_pos):
            action = btn["action"]
            if action == "fold":
                return ("fold", 0)
            elif action == "check":
                return ("check", 0)
            elif action == "call":
                return ("call", call_amount)
            elif action == "raise":
                return ("raise", raise_amount)
    return None
