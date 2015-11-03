#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from random import random
from pygame.sprite import *
from gameobject import *
from refresh import *

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
    cardback = GameObject(image=img)
    return cardback


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
    stepx = 0.2
    stepy = 0.1

    def __init__(self, deck=[]):
        self.n = len(deck)
        self.rect = Rect(DECK_POSITION, CARD_SIZE_DECK)

    def draw(self, surface):
        stepx = self.stepx
        stepy = self.stepy
        cardback = get_cardback().image
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

    @staticmethod
    def top_deck_animation(card_d, drawable, t=GLOBAL_FPS):
        card = card_from_dict(card_d)
        (x, y) = DECK_POSITION
        (w, h) = CARD_SIZE_DECK
        card.scale(w, h)
        card.set_pos(x, y)
        (dest_x, dest_y) = WINDOW_SIZE
        (dest_w, dest_h) = CARD_SIZE_DEFAULT
        dest_x = dest_x / 2 - dest_w / 2
        dest_y = dest_y / 2 - dest_h / 2

        cardback = get_cardback()
        cardback.scale(w, h)
        cardback.set_pos(x, y)
        move_and_scale_animation(cardback, (x + w // 2, y), (0, h), 0.2, drawable)

        card.set_rect((x + w // 2, y), (0, h))
        move_and_scale_animation(card, (x, y), (w, h), 0.2, drawable)

        move_and_scale_animation(card, (dest_x, dest_y), CARD_SIZE_DEFAULT, 0.4, drawable)
        delay_animation(card, 0.6, drawable)

    @staticmethod
    def on_click(gs, mouse_pos, drawable):
        cards = gs.top_deck()
        Deck.top_deck_animation(cards[0], drawable)
        gs.human_player().hand += cards


def delay_animation(obj, time, drawable):
    ticks = round(time * GLOBAL_FPS)
    drawable.append(obj)
    for t in range(ticks):
        refresh_scene(drawable)


def move_and_scale_animation(obj, new_pos, new_size, time, drawable):
    ticks = round(time * GLOBAL_FPS)
    (x1, y1) = obj.rect.topleft
    (w1, h1) = obj.rect.size
    (x2, y2) = new_pos
    (w2, h2) = new_size
    (vx, vy) = ((x2 - x1) / ticks, (y2 - y1) / ticks)
    (dw, dh) = ((w2 - w1) / ticks, (h2 - h1) / ticks)
    drawable.append(obj)
    (x, y) = (x1, y1)
    (w, h) = (w1, h1)
    for t in range(ticks):
        obj.set_pos(round(x), round(y))
        obj.scale(round(w), round(h))
        refresh_scene(drawable)
        (x, y) = (x + vx, y + vy)
        (w, h) = (w + dw, h + dh)
    obj.scale(w2, h2)
    obj.set_pos(x2, y2)
    refresh_scene(drawable)















