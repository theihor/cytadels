from globalvars import *
from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect
import pygame.transform
import pygame.font
import pygame.draw
import os.path
from gameobject import *
from loadimg import *


class Card(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.source_img = Surface(CARD_SIZE_DEFAULT)
        self.image = self.source_img
        self.rect = self.image.get_rect()

    def update(self, mouse_pos=None):
        if mouse_pos:
            if self.rect.collidepoint(mouse_pos):
                self.reset_img()
                self.set_pos(self.rect.x, WINDOW_SIZE[1]-self.rect.h)


class NoImgCard(Card):
    def __init__(self, card_dict):
        Card.__init__(self)
        self.name = card_dict['name']
        self.price = card_dict['price']
        self.value = card_dict['value']
        self.color = card_dict['color']
        self.init_img()

    def init_img(self):
        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 10)
        text = f.render(self.name, 1, COLOR_WHITE)
        r = text.get_rect()
        x = self.rect.w // 2 - r.w // 2
        y = self.rect.h * 4 // 10
        self.source_img.blit(text, (x, y))

        text = f.render(str(self.price) + '(' + str(self.value) + ')', 1, COLOR_WHITE)
        x = self.rect.w // 10
        y = self.rect.h // 40
        self.source_img.blit(text, (x, y))

        x = self.rect.w * 8 // 10
        y = self.rect.h // 8
        pygame.draw.circle(self.source_img, COLOR_CODE[COLOR_NAME[self.color]], (x, y), self.rect.h // 10)

        self.reset_img()


class ImgCard(Card):
    def __init__(self, image):
        self.source_img = image
        self.image = self.source_img
        self.rect = self.image.get_rect()

