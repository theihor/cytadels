from globalvars import *
from pygame.sprite import Sprite
from pygame import Surface
import pygame.transform
import pygame.font
import pygame.draw


class CardModel:
    def __init__(self, name='Undefined', price=0, value=0, color=0, img_path=None):
        self.name = name
        self.price = price
        self.value = value
        self.color = color
        self.img_path = img_path


class Card(CardModel, Sprite):
    def __init__(self, x=0, y=0, name='Undefined', price=0, value=0, color=0, img_path=None):
        CardModel.__init__(self, name, price, value, color, img_path)
        Sprite.__init__(self)
        self.pos = (x, y)
        self.source_img = Surface(CARD_SIZE_DEFAULT)
        self.img = self.source_img

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

    def get_rect(self):
        r = self.img.get_rect()
        (r.x, r.y) = self.pos
        return r


class NoImgCard(Card):
    def __init__(self, x=0, y=0, name='Undefined', price=0, value=0, color=0, img_path=None):
        Card.__init__(self, x, y, name, price, value, color, img_path)
        self.init_img()

    def init_img(self):
        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.get_rect().h // 10)
        text = f.render(self.name, 1, COLOR_WHITE)
        r = text.get_rect()
        x = self.get_rect().w // 2 - r.w // 2
        y = self.get_rect().h * 7 // 10
        self.source_img.blit(text, (x, y))

        text = f.render(str(self.price) + '(' + str(self.value) + ')', 1, COLOR_WHITE)
        x = self.get_rect().w // 10
        y = self.get_rect().h // 40
        self.source_img.blit(text, (x, y))

        x = self.get_rect().w * 8 // 10
        y = self.get_rect().h // 8
        pygame.draw.circle(self.source_img, COLOR_CODE[COLOR_NAME[self.color]], (x, y), self.get_rect().h // 10)






