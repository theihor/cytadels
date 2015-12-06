# LOGIC GLOBALS

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_TRANSPARENT = (42, 42, 42)  # WARNING: SOME ACTUAL COLOR USED HERE

GAME_COLOR = {
    "WHITE" :  0,
    "YELLOW" : 1,
    "BLUE" :   2,
    "GREEN" :  3,
    "RED" :    4,
    "PURPLE" : 5
}

COLOR_NAME = {
    0: "WHITE",
    1: "YELLOW",
    2: "BLUE",
    3: "GREEN",
    4: "RED",
    5: "PURPLE"
}

COLOR_CODE = {
    "WHITE":  COLOR_WHITE,
    "YELLOW": COLOR_YELLOW,
    "BLUE":   COLOR_BLUE,
    "GREEN":  COLOR_GREEN,
    "RED":    COLOR_RED,
    "PURPLE": COLOR_PURPLE
}

BUILDING_DECK_FILE_NAME = "building_deck.csv"
GLOBAL_FONT_FILE_NAME = 'fonts/OldEnglishFive.ttf'

COUNT_OF_PLAYERS = 7
HAND_SIZE = 4
COUNT_OF_SLOTS = 8

BONUS_COLORS = set(range(1, 6))

# pygame
GLOBAL_FPS = 60

WINDOW_SIZE = (1280, 720)

CARD_SIZE_DEFAULT = (300, 450)
CARD_SIZE_DECK = (100, 150)
CARD_SIZE_HAND = (80, 120)
CARD_SIZE_SLOT = (60, 90)
CARD_SIZE_MAIN_SLOT = (80, 120)
CARD_SIZE_CHOICE = (200, 300)

CHOICE_DECK_POSITION = ((WINDOW_SIZE[0] - CARD_SIZE_CHOICE[0]) // 2,
                        (WINDOW_SIZE[1] - CARD_SIZE_CHOICE[1]) // 2)

DECK_POSITION = (40, 520)
COINS_POSITION = (DECK_POSITION[0] + round(CARD_SIZE_DECK[0] * 1.4),
                  DECK_POSITION[1] + CARD_SIZE_DECK[1] // 5)

HAND_POSITION = (400, 640)
HAND_STEP = round(CARD_SIZE_HAND[0] * 0.05)
HAND_RECT_SIZE = (CARD_SIZE_HAND[0] * HAND_SIZE + HAND_STEP * (HAND_SIZE - 1), CARD_SIZE_HAND[1])

PLAYER_FRAME0_POS = (15, 20)
HUMAN_PLAYER_FRAME_POS = (300, 500)
HUMAN_PLAYER_FRAME_SIZE = (WINDOW_SIZE[0] - HUMAN_PLAYER_FRAME_POS[0],
                           WINDOW_SIZE[1] - HUMAN_PLAYER_FRAME_POS[1])

SHOW_CARD_POS = ((WINDOW_SIZE[0] - CARD_SIZE_DEFAULT[0]) // 2, (WINDOW_SIZE[1] - CARD_SIZE_DEFAULT[1]) // 2)

DRAWABLE = []

ROBBING_TIME = 0.4

PORTRAIT_SIZE = (80, 120)
PLAYER_PORTRAIT_SIZE = ((HUMAN_PLAYER_FRAME_SIZE[1] - 30) * 2 // 3, HUMAN_PLAYER_FRAME_SIZE[1] - 30)
