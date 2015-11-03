import pygame
from pygame import Surface
from globalvars import *
import os
from refresh import *


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image


def transparent_surface(size):
    img = Surface(size)
    img.fill(COLOR_TRANSPARENT)
    img.set_colorkey(COLOR_TRANSPARENT)
    return img

# loading textures
BACKGROUND_IMAGE = load_image("bg_table.png")
CARD_BACK_IMAGE = load_image("card_back.png")
CARD_TEMPLATE_IMAGE = load_image("card_template.png")

CARDS = ["tavern.png",
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
         "cathedral.png"]

CARD_IMAGES = {}
for card_image_name in CARDS:
    CARD_IMAGES[card_image_name] = load_image(os.path.join('cards', card_image_name))

#FONT = pygame.font.Font(GLOBAL_FONT_FILE_NAME)
COIN_MONEY_IMAGE = load_image("coin_yellow.png")
COIN_VALUE_IMAGE = load_image("coin_grey.png")

GEM_IMAGES = { 0: "grey.png",
               1: "yellow.png",
               2: "blue.png",
               3: "green.png",
               4: "red.png",
               5: "violet.png"}
for k in GEM_IMAGES:
    name = GEM_IMAGES[k]
    GEM_IMAGES[k] = load_image(name)