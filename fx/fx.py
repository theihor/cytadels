import pygame
import sys
import os
import math

pygame.init()

SIZE = (1280, 720)

COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)

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


class Card:
    def __init__(self, img_file_name, x = 0, y = 0):
        self.pos = (x, y)
        self.source_img = load_image(img_file_name)
        self.img = self.source_img
        self.rect = self.img.get_rect()

    def set_pos(self, x, y):
        self.pos = (x, y)

    def move(self, vector):
        (dx, dy) = vector
        (x, y) = self.pos
        self.set_pos(x + dx, y + dy)

    # def scale(self, proportion=(1, 1)):
    #     (px, py) = proportion
    #     size = (math.floor(self.rect.w * px), math.floor(self.rect.h * py))
    #     self.img = pygame.transform.smoothscale(self.img, size)
    #     self.rect = self.img.get_rect()

    def scaled(self, diff=(-2, -3)):
        (dx, dy) = diff
        size = (self.rect.w + dx, self.rect.h + dy)
        self.img = pygame.transform.smoothscale(self.source_img, size)
        self.rect = self.img.get_rect()

    def scale(self, w, h):
        size = (w, h)
        self.img = pygame.transform.smoothscale(self.source_img, size)
        self.rect = self.img.get_rect()

    def reset_img(self):
        self.img = self.source_img


the_card = Card('card2.bmp', 100, 100)
clock = pygame.time.Clock()


def refresh_scene(card):
    clock.tick(60)
    window.fill(COLOR_WHITE)
    show_card(card)
    pygame.display.flip()
    pass


def show_card(card):
    window.blit(card.img, card.pos)


def top_deck(card):
    card.set_pos(50, 300)
    card.scale(100, 30)
    v = (8, -7)
    scaling = (8, 15)
    print(card.rect.w, card.rect.h)
    while card.rect.w < 400 and card.rect.h < 600:
        #print(card.rect.w, card.rect.h)
        card.move(v)
        card.scaled(scaling)
        refresh_scene(card)
    card.reset_img()


top_deck(the_card)

while 1:
    refresh_scene(the_card)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            top_deck(the_card)


