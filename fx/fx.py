import pygame
from pygame.sprite import Sprite
import sys
import os
import math

pygame.init()

# create window
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Citadels')


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
        self.source_img = load_image(img_file_name)
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
the_card.scale(50, 75)
clock = pygame.time.Clock()


def refresh_scene(card):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    show_card(card)
    pygame.display.flip()
    pass


def show_card(card):
    window.blit(card.img, card.pos)


def top_deck(card):
    card.set_pos(50, 300)
    card.scale(50, 75)
    v = (8, -7)
    scaling = (10, 15)
    while card.get_rect().w < 400 and card.get_rect().h < 600:
        #print(card.rect.w, card.rect.h)
        card.move(v)
        card.scale_d(scaling)
        refresh_scene(card)
    card.reset_img()


while 1:
    refresh_scene(the_card)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            print(pygame.mouse.get_pos())
            print(the_card.get_rect())
            if the_card.get_rect().collidepoint(pygame.mouse.get_pos()):
                top_deck(the_card)


