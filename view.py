#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from math import ceil
from pygame.sprite import *
from gameobject import *
from animation import *


def card_from_dict(d):
    if d['image']:
        card = ImgCard(CARD_IMAGES[d['image']], d)
    else:
        card = NoImgCard(d)
    return card


class PlayerHand(Drawable):
    def __init__(self, hand=[]):
        GameObject.__init__(self, size=HAND_RECT_SIZE)
        self.set_pos(HAND_POSITION[0], HAND_POSITION[1])
        self.cards = []
        (card_w, card_h) = CARD_SIZE_HAND
        step = HAND_STEP
        (x, y) = HAND_POSITION
        for d in hand:
            card = card_from_dict(d)
            card.scale(card_w, card_h)
            card.set_pos(x, y)
            card.collide_rect = card.rect.copy()
            #self.cards.append(card)
            self.cards.append(CardInHand(card))
            x += card_w + round(step)
        self.draw_priority = 11

    def draw(self, surface):
        i = 1
        for card in self.cards:
            card.draw_priority = self.draw_priority + i
            i += 1

        pass

    def add_card(self, card):
        (card_w, card_h) = CARD_SIZE_HAND
        step = HAND_STEP
        (x, y) = HAND_POSITION
        for i in range(len(self.cards)):
            x += card_w + round(step)
        card.scale(card_w, card_h)
        card.set_pos(x, y)
        card.collide_rect = card.rect.copy()
        self.cards.append(CardInHand(card))


class Coins(Clickable):
    def __init__(self):
        Clickable.__init__(self, image=COINS_IMAGE)
        self.draw_priority = 98
        (x, y) = COINS_POSITION
        self.set_pos(x, y)

    def center_pos(self):
        (x, y) = self.pos()
        x += self.rect.w // 2
        y += self.rect.h // 2
        return x, y



class Deck(Clickable):
    stepx = 0.2
    stepy = 0.1

    def __init__(self, deck=[]):
        Clickable.__init__(self)
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
        whitecard = CARD_TEMPLATE_IMAGE
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
        (dest_x, dest_y) = SHOW_CARD_POS
        cardback = get_cardback()
        cardback.scale(w, h)
        cardback.set_pos(x, y)
        move_and_scale_animation(cardback, (x + w // 2, y), (0, h), 0.2, drawable)

        card.set_rect((x + w // 2, y), (0, h))
        move_and_scale_animation(card, (x, y), (w, h), 0.2, drawable)

        move_and_scale_animation(card, (dest_x, dest_y), CARD_SIZE_DEFAULT, 0.4, drawable)
        delay_animation(card, 0.6, drawable)
        move_and_scale_animation(card, hand_pos, CARD_SIZE_HAND, 0.3, drawable)

        hand = next(o for o in drawable if isinstance(o, PlayerHand))
        hand.add_card(card)

    def on_click(self, gs, drawable, mouse_pos=None):
        cards = gs.top_deck()
        n = len(gs.human_player().hand)
        (x, y) = HAND_POSITION
        x += n * (CARD_SIZE_HAND[0] + HAND_STEP)
        Deck.top_deck_animation(cards[0], drawable, (x, y))
        gs.human_player().hand += cards


class CardSlot(Drawable):
    def __init__(self, card=None, pos=None, main=False):
        self.main = main
        if main:
            Drawable.__init__(self, MAIN_SLOT_IMAGE.copy())
        else:
            Drawable.__init__(self, SLOT_IMAGE.copy())
        if pos: self.set_pos(pos[0], pos[1])
        self.card = card
        if card:
            (w, h) = self.card_size()
            (x, y) = self.pos()
            self.card.scale(w, h)
            self.card.set_pos(x + 4, y + 4)
        self.draw_priority = 80

    def on_mouse_over(self):
        if self.card:
            self.card.on_mouse_over()

    def set_card(self, card):
        self.card = card
        if self.main:
            (w, h) = CARD_SIZE_MAIN_SLOT
        else:
            (w, h) = CARD_SIZE_SLOT
        self.card.scale(w, h)
        (x, y) = self.card_pos()
        self.card.set_pos(x, y)
        self.card.collide_rect = self.rect

    def card_pos(self):
        (x, y) = self.pos()
        return x + 4, y + 4

    def card_size(self):
        if self.main:
            return CARD_SIZE_MAIN_SLOT
        else:
            return CARD_SIZE_SLOT


class PlayerFrame(Drawable):
    def __init__(self, player, killed=False):
        GameObject.__init__(self)
        self.player = player
        self.slots = []
        self.draw_priority = 90
        self.killed = killed

        self.init_slots()

    def slot_pos(self, number):
        (x, y) = (15, 15)
        for i in range(number):
            x += (SLOT_IMAGE.get_rect().w * 1.06)
            if i == 3:
                y += (SLOT_IMAGE.get_rect().h * 1.06)
                x = 15
        return x + self.rect.x, y + self.rect.y

    def init_slots(self):
        i = 0
        for slot in self.player.slots:
            card = card_from_dict(slot)
            slot_obj = CardSlot(card, self.slot_pos(i))
            self.slots.append(slot_obj)
            i += 1
        for i in range(len(self.slots), COUNT_OF_SLOTS):
            slot_obj = CardSlot(pos=self.slot_pos(i))
            self.slots.append(slot_obj)

    def portrait_pos(self):
        slot_w = SLOT_IMAGE.get_rect().w
        x = round(slot_w * 1.06 * 4)
        (w, h) = PORTRAIT_SIZE
        x += ((self.rect.w - x) - w) // 2
        y = self.rect.h // 2 - h // 2
        return x, y

    @staticmethod
    def score_pos(value_rect):
        slot_w = SLOT_IMAGE.get_rect().w
        x = round(slot_w * 1.06 * 4)
        x += (PLAYER_PORTRAIT_FRAME_IMAGE.get_rect().w // 2 - value_rect.w) // 2
        y = 12
        return x, y

    @staticmethod
    def money_icon_pos():
        slot_w = SLOT_IMAGE.get_rect().w
        x = round(slot_w * 1.06 * 4) + 15
        y = PLAYER_FRAME_IMAGE.get_rect().h - MONEY_ICON.get_rect().h - 12
        return x, y

    def global_money_icon_pos(self):
        (x1, y1) = self.money_icon_pos()
        (x, y) = self.pos()
        return x + x1, y + y1

    def money_pos(self, value_rect):
        (x, y) = self.money_icon_pos()
        x += MONEY_ICON.get_rect().h + 4
        y += (MONEY_ICON.get_rect().h - value_rect.h) // 2
        return x, y

    def cards_icon_pos(self):
        (x, y) = self.money_icon_pos()
        x += PLAYER_PORTRAIT_FRAME_IMAGE.get_rect().w // 2
        return x, y

    def global_cards_icon_pos(self):
        (x1, y1) = self.cards_icon_pos()
        (x, y) = self.pos()
        return x + x1, y + y1

    def cards_value_pos(self, value_rect):
        (x, y) = self.cards_icon_pos()
        x += CARDS_ICON.get_rect().h + 1
        y += (CARDS_ICON.get_rect().h - value_rect.h) // 2
        return x, y

    def adjust_portrait(self):
        (w, h) = PORTRAIT_SIZE
        self.portrait.scale(w, h)
        (x, y) = self.global_portrait_pos()
        self.portrait.set_pos(x, y)

        self.portrait.collide_rect = self.portrait.rect.copy()

    def global_portrait_pos(self):
        (x, y) = self.portrait_pos()
        print(x, y)
        print(self.pos())
        pos = self.pos()
        x += pos[0]
        y += pos[1]
        return x, y

    def put_card_in_slots(self, card, scene):
        slot = next(s for s in self.slots if not s.card)
        slot.set_card(card)
        scene['slot_cards'].append(card)

    def next_slot(self):
        return next(s for s in self.slots if not s.card)

    def draw(self, surface):
        self.reset_img()

        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 10)
        text = f.render(str(self.player.base_score()), 1, COLOR_BLACK)
        self.image.blit(text, self.score_pos(text.get_rect()))

        self.image.blit(MONEY_ICON, self.money_icon_pos())
        text = f.render(str(self.player.money), 1, COLOR_BLACK)
        self.image.blit(text, self.money_pos(text.get_rect()))

        self.image.blit(CARDS_ICON, self.cards_icon_pos())
        text = f.render(str(len(self.player.hand)), 1, COLOR_BLACK)
        self.image.blit(text, self.cards_value_pos(text.get_rect()))

        surface.blit(self.image, self.rect)


class AIPlayerFrame(PlayerFrame):
    def __init__(self, player, number, killed=False):
        GameObject.__init__(self, PLAYER_FRAME_IMAGE.copy())
        self.player = player
        self.slots = []
        self.draw_priority = 90
        self.killed = killed

        (x, y) = self.frame_pos(number)
        self.set_pos(x, y)

        self.init_slots()

        self.portrait = CharacterCard(self.player.role[0], self)

        self.adjust_portrait()

    @staticmethod
    def frame_pos(number):
        (x, y) = PLAYER_FRAME0_POS
        for i in range(number):
            x += (PLAYER_FRAME_IMAGE.get_rect().w * 1.03)
            if i == 2:
                y += (PLAYER_FRAME_IMAGE.get_rect().h * 1.05)
                x = PLAYER_FRAME0_POS[0]
        return x, y


class HumanPlayerFrame(PlayerFrame):
    def __init__(self, player, killed=False):
        PlayerFrame.__init__(self, player, killed=killed)
        self.source_img = transparent_surface(HUMAN_PLAYER_FRAME_SIZE)
        self.reset_img()
        (x, y) = HUMAN_PLAYER_FRAME_POS
        self.set_pos(x, y)

        self.portrait = CharacterCard(self.player.role[0], self)
        self.adjust_portrait()

    @staticmethod
    def slot_pos(number):
        (x, y) = HUMAN_PLAYER_FRAME_POS
        for i in range(number):
            x += (MAIN_SLOT_IMAGE.get_rect().w * 1.06)
        return x, y

    def init_slots(self):
        i = 0
        for slot in self.player.slots:
            card = card_from_dict(slot)
            slot_obj = CardSlot(card, self.slot_pos(i), main=True)
            self.slots.append(slot_obj)
            i += 1

        for i in range(len(self.slots), COUNT_OF_SLOTS):
            slot_obj = CardSlot(pos=self.slot_pos(i), main=True)
            self.slots.append(slot_obj)

    def portrait_pos(self):
        x = self.rect.w - PLAYER_PORTRAIT_SIZE[0] - 20
        y = self.rect.h - PLAYER_PORTRAIT_SIZE[1] - 15
        return x, y

    def score_pos(self, value_rect):
        slot_w = MAIN_SLOT_IMAGE.get_rect().w
        x = round(slot_w * 1.06 * 8)
        x = (self.portrait_pos()[0] + x) // 2 - value_rect.w // 2
        y = 10
        return x, y

    def money_icon_pos(self):
        slot_w = MAIN_SLOT_IMAGE.get_rect().w
        x = round(slot_w * 1.06 * 8)
        x += 5
        y = COIN_MONEY_IMAGE.get_rect().h + 25
        return x, y

    def adjust_portrait(self):
        (w, h) = PLAYER_PORTRAIT_SIZE
        self.portrait.scale(w, h)
        (x, y) = self.global_portrait_pos()
        self.portrait.set_pos(x, y)

        self.portrait.collide_rect = self.portrait.rect.copy()

    def draw(self, surface):
        self.reset_img()

        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 10)
        text = f.render(str(self.player.base_score()), 1, COLOR_BLACK)
        self.image.blit(text, self.score_pos(text.get_rect()))

        self.image.blit(MONEY_ICON, self.money_icon_pos())
        text = f.render(str(self.player.money), 1, COLOR_BLACK)
        self.image.blit(text, self.money_pos(text.get_rect()))

        surface.blit(self.image, self.rect)




