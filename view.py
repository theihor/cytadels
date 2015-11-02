#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from random import random
from pygame.sprite import *
from gameobject import *

DECK_POSITION = (40, 520)
HAND_POSITION = (300, 550)





def card_from_dict(d):
    card = NoImgCard(name = d['name'],
                     price = d['price'],
                     value = d['value'],
                     color = d['color'])
    return card


def get_cardback():
    #img = Surface(CARD_SIZE_DEFAULT)
    #img.fill(COLOR_PURPLE)
    img = load_image("port.png")
    return img


class PlayerHand:
    def __init__(self, hand=[]):
        self.cards = []
        (card_w, card_h) = CARD_SIZE_HUMAN_PLAYER_HAND
        step = card_w * 0.05
        (x, y) = HAND_POSITION
        for d in hand:
            card = card_from_dict(d)
            card.scale(card_w, card_h)
            card.set_pos(x, y)
            self.cards.append(card)
            x += card_w + round(step)

    def update(self, mouse_pos):
        for card in self.cards:
            card.update(mouse_pos)

    def draw(self, surface):
        for card in reversed(self.cards):
            surface.blit(card.image, card.rect)


class Deck:
    def __init__(self, deck=[]):
        self.n = len(deck)

    def draw(self, surface):
        stepx = 0.2
        stepy = 0.1
        cardback = get_cardback()
        cardback = pygame.transform.smoothscale(cardback, CARD_SIZE_DECK)
        (w, h) = cardback.get_size()
        w += ceil(2 * self.n * abs(stepx))
        h += ceil(2 * self.n * abs(stepy))
        (x, y) = DECK_POSITION
        if stepx < 0:
            x += (2 * self.n - 1) * stepx
        if stepy > 0:
            y += (2 * self.n - 1) * stepy
        whitecard = load_image("card_template.png")
        whitecard = pygame.transform.smoothscale(whitecard, CARD_SIZE_DECK)
        for i in range(self.n * 2):
            if i % 2 == 0 or i == 0 or i == self.n * 2 - 1:
                surface.blit(cardback, (round(x), round(y)))
            else:
                surface.blit(whitecard, (round(x), round(y)))
            x += stepx
            y -= stepy
        pass










