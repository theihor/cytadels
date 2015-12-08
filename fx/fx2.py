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
GLOBAL_FPS = 60 
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)

def load_image(name, colorkey=None):
    fullname = name
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image

clock = pygame.time.Clock()


def effect_step(img):
    mx, my = pygame.mouse.get_pos()
    (x, y) = img
    pass


#img = load_image("button.png")
#img.fill(COLOR_BLACK)
#img.convert_alpha()
#img.lock()





def show_card(card):
    window.blit(card.img, card.pos)


def refresh_scene(card):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    show_card(card)
    pygame.display.flip()
    pass


f = True

def effect_step(img):
    global f
    a = pixels_alpha(img)

   # j = len(a[0]) // 2
   # for i in range(5, len(a) - 5):
   #     if j > 5 and j < len(a[i]) - 5:
   #         p = 0.2
   #         if random() < p:
   #             j += randrange(3) - 1 
   #         a[i][j] = 0

    img2 = Surface(img.get_rect().size, pygame.SRCALPHA)
    img2.fill((255, 255, 255))
    b = pixels_alpha(img2)
    #
    # for i in range(len(a)):
    #     b[i][0] = 0
    #     b[i][len(a[i]) -1] = 0
    # for j in range(len(a[0])):
    #     b[0][j] = 0
    #     b[len(a)-1][j] = 0

    (w, h) = img.get_rect().size
    (cx, cy) = (w / 2, h / 2)
    d = max(w, h)
    for x in range(len(b)):
        for y in range(len(b[x])):
            k = math.sqrt(sqr(float(x) - cx) + sqr(float(y) - cy))
            if k > d: b[x][y] = 0
            else:
            #print(k)
                b[x][y] = round(k / d * 200.0)

    # n = len(a)
    # m = len(a[0])
    # for k1 in range(n // 2 - 1):
    #     for k2 in range(m // 2 - 1):
    #         i = n // 2 - k1
    #         j = m // 2 - k2
    #         while i < n // 2 + k1:
    #             if a[i][j] == 0:
    #                 x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
    #                         a[i][j-1], a[i][j], a[i][j+1],
    #                         a[i+1][j-1], a[i+1][j], a[i+1][j+1])
    #                 b[i][j] = x * 7 // 10
    #             else:
    #                 b[i][j] = 0
    #             i += 1
    #         while j < m // 2 + k2:
    #             if a[i][j] == 0:
    #                 x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
    #                         a[i][j-1], a[i][j], a[i][j+1],
    #                         a[i+1][j-1], a[i+1][j], a[i+1][j+1])
    #                 b[i][j] = x * 7 // 10
    #             else:
    #                 b[i][j] = 0
    #             j += 1
    #         while i > n // 2 - k1:
    #             if a[i][j] == 0:
    #                 x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
    #                         a[i][j-1], a[i][j], a[i][j+1],
    #                         a[i+1][j-1], a[i+1][j], a[i+1][j+1])
    #                 b[i][j] = x * 7 // 10
    #             else:
    #                 b[i][j] = 0
    #             i -= 1
    #         while j > m // 2 - k2:
    #             if a[i][j] == 0:
    #                 x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
    #                         a[i][j-1], a[i][j], a[i][j+1],
    #                         a[i+1][j-1], a[i+1][j], a[i+1][j+1])
    #                 b[i][j] = x * 7 // 10
    #             else:
    #                 b[i][j] = 0
    #             j -= 1

    #
    # for i in range(1, len(a) - 1):
    #     for j in range(1, len(a[i]) - 1):
    #         if a[i][j] < 20:
    #              x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
    #                      a[i][j-1], a[i][j], a[i][j+1],
    #                      a[i+1][j-1], a[i+1][j], a[i+1][j+1])
    #              b[i][j] = x * 6 // 10 #+ randrange(20) - 10
    #         else:
    #             b[i][j] = 0

    #if a[0][0] == 255: f = False
    #if a[0][0] == 0: f = True
    #if f: a += 1
    #else: a -= 1

    a = None
    b = None
    img2.blit(img, (0,0))
    return img

picture = load_image("button.png")

(w,h) = picture.get_rect().size
#s = max(w,h) + 10
img = Surface((round(w * 1.5) , round(h * 1.5)), pygame.SRCALPHA)
img.fill(COLOR_WHITE)
a = pixels_alpha(img)
#print(a)


(cx, cy) = img.get_rect().size
cx //= 2
cy //= 2
print(cx,cy)
d = max(w, h) / 2 #math.sqrt(cx * cx + cy * cy)

def sqr(x):
    return x * x

for x in range(len(a)):
    for y in range(len(a[x])):
        k = math.sqrt(sqr(100 * (float(x) - cx) / cx) + sqr(100 * (float(y) - cy) / cy))
        if k > 100: a[x][y] = 0
        else:
            a[x][y] = 255 - round(k / 100.0 * 255.0)

a = None

#image = picture.copy()
pos = ((img.get_rect().w - picture.get_rect().w) // 2, (img.get_rect().h - picture.get_rect().h) // 2)
img.blit(picture, pos)

while 1:
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_BLACK)
    
    #img = Surface((200, 300), pygame.SRCALPHA)
    #img.fill(COLOR_BLACK)
    #img = effect_step(img)
    #print("tick")
    window.blit(img, (200, 100))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            (mx, my) = pygame.mouse.get_pos()
            print(mx, my)
