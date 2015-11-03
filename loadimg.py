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
