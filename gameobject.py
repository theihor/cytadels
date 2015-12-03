import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from pygame.sprite import *
from pygame import Surface


def transparent_surface(size):
    img = Surface(size)
    img.fill(COLOR_TRANSPARENT)
    img.set_colorkey(COLOR_TRANSPARENT)
    return img


class GameObject:
    def __init__(self, image=None, size=None):
        self.source_img = transparent_surface((0, 0))
        if image:
            self.source_img = image
        else:
            if size:
                self.source_img = transparent_surface(size)
            else:
                self.source_img = transparent_surface((0, 0))
        self.image = self.source_img
        self.rect = self.image.get_rect()
        if size:
            self.scale(size[0], size[1])

    def pos(self):
        return self.rect.topleft

    def size(self):
        return self.rect.size

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
        self.image = self.source_img.copy()
        self.update_rect_size()

    def set_rect(self, pos, size):
        (x, y) = pos
        self.set_pos(x ,y)
        (w, h) = size
        self.scale(w, h)


class Drawable(GameObject):
    def __init__(self, image=None, size=None):
        GameObject.__init__(self, image=image, size=size)
        self.draw_priority = 100

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Collidable(Drawable):
    def __init__(self, image=None, size=None):
        GameObject.__init__(self, image=image, size=size)
        self.collide_rect = self.rect

    def collides(self, pos):
        return self.collide_rect.collidepoint(pos)


class Updatable(Collidable):
    def on_mouse_over(self):
        pass

    def on_mouse_out(self):
        pass


class Clickable(Updatable):
    def on_click(self, gs, drawable):
        pass



