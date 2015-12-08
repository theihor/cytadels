import pygame
import sys
import math
from globalvars import *
from card import *
from pygame.sprite import *
from pygame import Surface
from loadimg import *
import pygame.surfarray as surfa


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
        #self.rect = self.image.get_rect()
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


def sqr(x): return x * x

class Drawable(GameObject):
    def __init__(self, image=None, size=None):
        GameObject.__init__(self, image=image, size=size)
        self.draw_priority = 100
        self.highlighted = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def highlight(self):
        if not self.highlighted:
            (x, y) = self.pos()
            (w, h) = self.rect.size
            (lw, lh) = (round(w * 1.5), round(h * 1.5))

            img = Surface((lw, lh), pygame.SRCALPHA)
            img.fill(COLOR_WHITE)
            a = surfa.pixels_alpha(img)
            d = max(lw, lh) / 2
            (cx, cy) = (lw // 2, lh // 2)

            for i in range(len(a)):
                for j in range(len(a[i])):
                    k = math.sqrt(sqr(100.0 * (i - cx) / cx) + sqr(100.0 * (j - cy) / cy))
                    if k > 100: a[i][j] = 0
                    else: a[i][j] = 255 - round(k / 100.0 * 255.0)

            a = None

            img.blit(self.image, ((lw - w) // 2, (lh - h) // 2))
            self.image = img

            self.set_pos(x - (lw - w) // 2, y - (lh - h) // 2)
            self.highlighted = True

    def unhighlight(self):
        if self.highlighted:
            (x, y) = self.pos()
            (w, h) = self.size()
            (lw, lh) = (round(w / 1.5), round(h / 1.5))
            (dx, dy) = ((w - lw) // 2, (h - lh) // 2)
            self.set_pos(x + dx, y + dy)
            self.reset_img()
            self.highlighted = False


class Collidable(Drawable):
    def __init__(self, image=None, size=None):
        Drawable.__init__(self, image=image, size=size)
        self.collide_rect = self.rect

    def collides(self, pos):
        return self.collide_rect.collidepoint(pos)


class Updatable(Collidable):
    def on_mouse_over(self):
        pass

    def on_mouse_out(self):
        pass


class Clickable(Updatable):
    def on_click(self, gs, drawable, mouse_pos=None):
        pass



