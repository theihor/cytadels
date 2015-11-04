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
        #x = WINDOW_SIZE[0] // 2
        #x -= card_w // 2
        #x -= (card_w + round(step)) * (len(hand) - 1) // 2
        for d in hand:
            card = card_from_dict(d)
            card.scale(card_w, card_h)
            card.set_pos(x, y)
            self.cards.append(card)
            x += card_w + round(step)
        self.draw_priority = 9

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
        (w, h) = CARD_SIZE_DECK
        w += round(2 * self.n * self.stepx)
        h += round(2 * self.n * self.stepy)
        self.rect = Rect(DECK_POSITION, (w, h))
        self.draw_priority = 99

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


class CardSlot(GameObject):
    def __init__(self, card=None, pos=None, main=False):
        self.main = main
        if main:
            GameObject.__init__(self, MAIN_SLOT_IMAGE.copy())
        else:
            GameObject.__init__(self, SLOT_IMAGE.copy())
        if pos: self.set_pos(pos[0], pos[1])
        self.card = card
        if card:
            if self.main:
                (w, h) = CARD_SIZE_MAIN_SLOT
            else:
                (w, h) = CARD_SIZE_SLOT
            (x, y) = self.pos()
            self.card.scale(w, h)
            self.card.set_pos(x + 4, y + 4)
        self.draw_priority = 80

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            #print(mouse_pos)
            if self.card:
                self.card.update(mouse_pos)


class PlayerFrame(GameObject):
    def __init__(self, player, number):
        GameObject.__init__(self, PLAYER_FRAME_IMAGE)
        self.player = player
        self.slots = []
        (x, y) = self.frame_pos(number)
        self.set_pos(x, y)
        self.init_slots(player)
        self.draw_priority = 90

        self.portrait = PORTRAIT_UNKNOWN_IMAGE


    @staticmethod
    def frame_pos(number):
        (x, y) = PLAYER_FRAME0_POS
        for i in range(number):
            x += (PLAYER_FRAME_IMAGE.get_rect().w * 1.03)
            if i == 2:
                y += (PLAYER_FRAME_IMAGE.get_rect().h * 1.05)
                x = PLAYER_FRAME0_POS[0]
        return x, y

    def slot_pos(self, number):
        (x, y) = (15, 15)
        for i in range(number):
            x += (SLOT_IMAGE.get_rect().w * 1.06)
            if i == 3:
                y += (SLOT_IMAGE.get_rect().h * 1.06)
                x = 15
        return x + self.rect.x, y + self.rect.y

    def init_slots(self, player):
        i = 0
        for slot in player.slots:
            card = card_from_dict(slot)
            slot_obj = CardSlot(card, self.slot_pos(i))
            self.slots.append(slot_obj)
            i += 1

        for i in range(len(self.slots), COUNT_OF_SLOTS):
            slot_obj = CardSlot(pos=self.slot_pos(i))
            self.slots.append(slot_obj)

    def portrait_pos(self):
        (x, y) = self.pos()
        slot_w = SLOT_IMAGE.get_rect().w
        x += round(slot_w * 1.06 * 4) + 13
        y += self.rect.h // 2 - PLAYER_PORTRAIT_FRAME_IMAGE.get_rect().h // 2
        return x, y

    def score_pos(self):
        (x, y) = self.pos()
        slot_w = SLOT_IMAGE.get_rect().w
        x += round(slot_w * 1.06 * 4) + 12
        y = 18
        return x, y


    def draw(self, surface):
        surface.blit(self.image, self.rect)

        for slot in self.slots:
            slot.draw(surface)

        pos = self.portrait_pos()
        surface.blit(PLAYER_PORTRAIT_FRAME_IMAGE, pos)
        surface.blit(self.portrait, pos)

        # f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 6)
        # text = f.render(str(self.player.base_score()), 1, COLOR_BLACK)
        # surface.blit(text, self.score_pos())






class HumanPlayerFrame:
    def __init__(self, player):
        self.slots = []
        self.init_slots(player)

    @staticmethod
    def slot_pos(number):
        (x, y) = HUMAN_PLAYER_FRAME_POS
        for i in range(number):
            x += (MAIN_SLOT_IMAGE.get_rect().w * 1.06)
        return x, y

    def init_slots(self, player):
        i = 0
        for slot in player.slots:
            card = card_from_dict(slot)
            slot_obj = CardSlot(card, self.slot_pos(i), main=True)
            self.slots.append(slot_obj)
            i += 1

        for i in range(len(self.slots), COUNT_OF_SLOTS):
            slot_obj = CardSlot(pos=self.slot_pos(i), main=True)
            self.slots.append(slot_obj)

