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

img = Surface((200, 300), pygame.SRCALPHA)
img = load_image("button.png")
#img.fill(COLOR_BLACK)
#img.convert_alpha()
#img.lock()
print(img.get_masks())




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
    img2.fill((0, 0, 255))
    b = pixels_alpha(img2)

    for i in range(len(a)):
        b[i][0] = 0
        b[i][len(a[i]) -1] = 0

    for i in range(1, len(a) - 1):
        for j in range(1, len(a[i]) - 1):
            if a[i][j] < 20:
                x = max(a[i-1][j-1], a[i-1][j], a[i-1][j+1],
                        a[i][j-1], a[i][j], a[i][j+1],
                        a[i+1][j-1], a[i+1][j], a[i+1][j+1])
                b[i][j] = x * 6 // 10 #+ randrange(20) - 10
            else: 
                b[i][j] = 0

    #if a[0][0] == 255: f = False
    #if a[0][0] == 0: f = True
    #if f: a += 1
    #else: a -= 1

    a = None
    b = None
    img.blit(img2, (0,0))

a = pixels_alpha(img)
print(a)
a = None

while 1:
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    
    #img = Surface((200, 300), pygame.SRCALPHA)
    #img.fill(COLOR_BLACK)
    effect_step(img)

    window.blit(img, (100, 100))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            (mx, my) = pygame.mouse.get_pos()
            print(mx, my)
