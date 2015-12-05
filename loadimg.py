import pygame
from pygame import Surface
from globalvars import *
from refresh import *
from characters import CHARACTERS
import os



def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image


# loading textures
BACKGROUND_IMAGE = load_image("bg_table.png")
CARD_BACK_IMAGE = load_image("card_back.png")
CARD_TEMPLATE_IMAGE = load_image("card_template.png")

CARDS = [ "tavern.png",
          "market.png",
          "port.png",
          "harbor.png",
          "castle.png",
          "palace.png",
          "watchtower.png",
          "prison.png",
          "arena.png",
          "church.png",
          "monastery.png",
          "cathedral.png",
          "observatory.png",
          "ghost_house.png",
          "lab.png",
          "fort.png",
          "dragon_gate.png",
          "university.png",
          "cemetery.png",
          "magic_school.png",
          "library.png",
          "forge.png",
          "great_wall.png",
          "park.png",
          "temple.png",
          "armory.png",
          "circus.png"
          ]

CARD_IMAGES = {}
for card_image_name in CARDS:
    CARD_IMAGES[card_image_name] = load_image(os.path.join('cards', card_image_name))

CHARACTER_PNGS = [ "assassin.png", "thief.png", "magician.png", "king.png",
                   "priest.png", "merchant.png", "architect.png", "warlord.png" ]

CHARACTER_IMAGES = {}
for i in range(len(CHARACTERS)):
    CHARACTER_IMAGES[CHARACTERS[i][0]] = load_image(os.path.join('characters', CHARACTER_PNGS[i]))

CHARACTER_GEMS = { 'Assassin': 0,
                   'Thief': 0,
                   'Wizard': 0,
                   'King': 1,
                   'Bishop': 2,
                   'Merchant': 3,
                   'Architect': 0,
                   'Warlord': 4 }

#FONT = pygame.font.Font(GLOBAL_FONT_FILE_NAME)
COIN_MONEY_IMAGE = load_image("coin_yellow.png")
COIN_VALUE_IMAGE = load_image("coin_grey.png")

GEM_IMAGES = { 0: "grey.png",
               1: "yellow.png",
               2: "blue.png",
               3: "green.png",
               4: "red.png",
               5: "violet.png" }

for k in GEM_IMAGES:
    name = GEM_IMAGES[k]
    GEM_IMAGES[k] = load_image(name)

PLAYER_FRAME_IMAGE = load_image('frame.png')
SLOT_IMAGE = load_image("slot_card.png")
MAIN_SLOT_IMAGE = load_image("main_slot_card.png")

PLAYER_PORTRAIT_FRAME_IMAGE = load_image("oval_frame.png")
MONEY_ICON = load_image("coin_on_table.png")
CARDS_ICON = load_image("card_on_table.png")

PORTRAIT_UNKNOWN_IMAGE = load_image("unknown_hero.png")


def scene_objects(scene):
    objects = []
    for key in scene:
        objects += scene[key]
    return objects
