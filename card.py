from globalvars import *
from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect
import pygame.transform
import pygame.font
import pygame.draw
import os.path
from gameobject import *




class CardModel:
    def __init__(self, name='Undefined', price=0, value=0, color=0, img_path=None):
        self.name = name
        self.price = price
        self.value = value
        self.color = color
        self.img_path = img_path


class Card(CardModel, GameObject):
    def __init__(self, x=0, y=0, name='Undefined', price=0, value=0, color=0, img_path=None):
        CardModel.__init__(self, name, price, value, color, img_path)
        GameObject.__init__(self)
        self.pos = (x, y)
        self.source_img = Surface(CARD_SIZE_DEFAULT)
        self.image = self.source_img
        self.rect = self.image.get_rect()
        self.highlighted = False

    def update(self, mouse_pos=None):
        if mouse_pos:
            print(mouse_pos)
            print(self.rect)
            if self.rect.collidepoint(mouse_pos):
                self.reset_img()
                self.set_pos(self.rect.x, WINDOW_SIZE[1]-self.rect.h)


    # def highlight(self):
    #     self.highlighted = True
    #     img = self.image
    #     (w, h) = img.get_size()
    #     k = 1.1
    #     shift = ceil(w * (k - 1) / 2)
    #     w = round(w * k)
    #     h = round(h * k)
    #     light = transparent_surface((w, h))
    #     pygame.draw.rect(light, COLOR_YELLOW, light.get_rect(), width=10)
    #     light.blit(img, (shift, shift))
    #     self.image = light
    #     (x, y) = self.pos()
    #     self.set_pos(x - shift, x + shift)
    #
    # def unhighlight(self):
    #     self.highlighted = False
    #     img = self.image
    #     (w, h) = img.get_size()
    #     k = 1.1
    #     shift = ceil(w * (k - 1) / 2)
    #     w = round(w * k)
    #     h = round(h * k)
    #     light = transparent_surface((w, h))
    #     pygame.draw.rect(light, COLOR_YELLOW, light.get_rect(), width=10)
    #     light.blit(img, (shift, shift))
    #     self.image = light
    #     self.rect = Rect((self.rect.x - shift, self.rect.y - shift), light.get_size())


        #if highlight and not self.highlighted: self.highlight()
        #if not highlight and self.highlighted: self.unhighlight()


class NoImgCard(Card):
    def __init__(self, x=0, y=0, name='Undefined', price=0, value=0, color=0, img_path=None):
        Card.__init__(self, x, y, name, price, value, color, img_path)
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
    def __init__(self, img_file_name, x=0, y=0):
        Sprite.__init__(self)
        self.source_img = load_image(img_file_name)
        self.image = self.source_img
        self.rect = self.image.get_rect()
        self.set_pos(x, y)
        self.picked = False








