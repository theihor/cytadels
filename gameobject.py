import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from random import random
from pygame.sprite import *

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

class GameObject(Sprite):
    def __init__(self, size=(0, 0), image=None):
        Sprite.__init__(self)
        self.children = Group()
        self.source_img = None
        if image:
            self.source_img = image
        else:
            self.source_img = transparent_surface(size)
        self.image = self.source_img
        self.rect = self.image.get_rect()
        self.update()

    def update(self, mouse_pos=None):
        #print("updated", self)
        if mouse_pos:
            (mx, my) = mouse_pos
            (x, y) = self.pos()
            self.children.update((mx - x, my - y))
        self.children.update()
        self.children.draw(self.image)

    def add_object(self, obj):
        self.children.add(obj)
        self.update()

    def pos(self):
        return self.rect.topleft

    def set_pos(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_rect_size(self):
        r = self.image.get_rect()
        self.rect.w = r.w
        self.rect.h = r.h

    def move(self, vector):
        (x, y) = vector
        self.rect.move_ip(x, y)

    def scale_d(self, diff=(0, 0)):
        (dx, dy) = diff
        size = (self.rect.w + dx, self.rect.h + dy)
        self.image = pygame.transform.smoothscale(self.source_img, size)
        self.update_rect_size()

    def scale(self, w, h):
        size = (w, h)
        self.image = pygame.transform.smoothscale(self.source_img, size)
        self.update_rect_size()

    def reset_img(self):
        self.image = self.source_img
        self.update_rect_size()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_rect(self, pos, size):
        (x, y) = pos
        self.set_pos(x ,y)
        (w, h) = size
        self.scale(w, h)
