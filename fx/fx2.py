#!/usr/bin/python3
import pygame
from pygame.sprite import Sprite
from pygame import Surface
import sys
import os
import math
from pygame.surfarray import *
from random import *

pygame.init()

SIZE = (600, 600)

# create window
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Citadels')
GLOBAL_FPS = 60
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)

def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image


class Card(Sprite):
    def __init__(self, img_file_name, x=0, y=0):
        Sprite.__init__(self)
        self.pos = (x, y)
        self.source_img = Surface((200, 300))
        self.source_img.fill(COLOR_BLACK)
        self.source_img.convert_alpha()
        #self.source_img.set_alpha(100)
        self.img = self.source_img
        self.picked = False

    def set_pos(self, x, y):
        self.pos = (x, y)

    def move(self, vector):
        (dx, dy) = vector
        (x, y) = self.pos
        self.set_pos(x + dx, y + dy)

    def scale_d(self, diff=(0, 0)):
        (dx, dy) = diff
        size = (self.get_rect().w + dx, self.get_rect().h + dy)
        self.img = pygame.transform.smoothscale(self.source_img, size)

    def scale(self, w, h):
        size = (w, h)
        self.img = pygame.transform.smoothscale(self.source_img, size)

    def reset_img(self):
        self.img = self.source_img

    def set_picked(self, picked=True):
        self.picked = picked

    def get_rect(self):
        r = self.img.get_rect()
        (r.x, r.y) = self.pos
        return r

the_card = Card('card2.bmp', 50, 300)
the_card.set_pos(100, 100)
clock = pygame.time.Clock()


def effect_step(img):
    mx, my = pygame.mouse.get_pos()
    (x, y) = img
    pass

img = Surface((200, 300), pygame.SRCALPHA)
#img.convert_alpha()
#img.lock()
print(img.get_masks())

# for x in range(img.get_rect().h // 2):
#     for y in range(img.get_rect().h // 2):
#         img.set_at((x,y), (0,128,0,128))




def show_card(card):
    window.blit(card.img, card.pos)


def refresh_scene(card):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    show_card(card)
    pygame.display.flip()
    pass


f = True
while 1:
    a = pixels_alpha(img)

    if a[0][0] == 255: f = False
    if a[0][0] == 0: f = True
    if f: a += 1
    else: a -= 1
    a = None
    img.unlock()

    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    #x = img.copy()
    window.blit(img, (100, 100))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            (mx, my) = pygame.mouse.get_pos()
            (x, y) = the_card.pos
