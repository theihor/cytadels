#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from random import random
from pygame.sprite import *
from gameobject import *
from animation import *
from loadimg import *


def card_from_dict(d):
    if d['image']:
        card = ImgCard(CARD_IMAGES[d['image']], d)
    else:
        card = NoImgCard(d)
    return card


def get_cardback():
    return GameObject(CARD_BACK_IMAGE)


class PlayerHand:
    def __init__(self, hand=[]):
        self.cards = []
        (card_w, card_h) = CARD_SIZE_HAND
        step = HAND_STEP
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
    def top_deck_animation(card_d, drawable, hand_pos):
        card = card_from_dict(card_d)
        (x, y) = DECK_POSITION
        (w, h) = CARD_SIZE_DECK
        card.scale(w, h)
        card.set_pos(x, y)
        (dest_x, dest_y) = WINDOW_SIZE
        # (dest_w, dest_h) = CARD_SIZE_DEFAULT
        # dest_x = dest_x / 2 - dest_w / 2
        # dest_y = dest_y / 2 - dest_h / 2
        (dest_x, dest_y) = (300, 20)
        cardback = get_cardback()
        cardback.scale(w, h)
        cardback.set_pos(x, y)
        move_and_scale_animation(cardback, (x + w // 2, y), (0, h), 0.2, drawable)

        card.set_rect((x + w // 2, y), (0, h))
        move_and_scale_animation(card, (x, y), (w, h), 0.2, drawable)

        move_and_scale_animation(card, (dest_x, dest_y), CARD_SIZE_DEFAULT, 0.4, drawable)
        delay_animation(card, 0.6, drawable)
        move_and_scale_animation(card, hand_pos, CARD_SIZE_HAND, 0.3, drawable)

    @staticmethod
    def on_click(gs, mouse_pos, drawable):
        cards = gs.top_deck()
        n = len(gs.human_player().hand)
        (x, y) = HAND_POSITION
        x += n * (CARD_SIZE_HAND[0] + HAND_STEP)
        Deck.top_deck_animation(cards[0], drawable, (x, y))
        gs.human_player().hand += cards

















