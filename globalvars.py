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
    "WHITE" :  COLOR_WHITE,
    "YELLOW" : COLOR_YELLOW,
    "BLUE" :   COLOR_BLUE,
    "GREEN" :  COLOR_GREEN,
    "RED" :    COLOR_RED,
    "PURPLE" : COLOR_PURPLE
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

DECK_POSITION = (40, 520)

HAND_POSITION = (250, 640)
HAND_STEP = round(CARD_SIZE_HAND[0] * 0.05)

PLAYER_FRAME0_POS = (15, 20)
HUMAN_PLAYER_FRAME_POS = (220, 500)

DRAWABLE = []
