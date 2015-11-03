#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from game_init import init_game
from view import *
from refresh import *

pygame.init()

# create window

pygame.display.set_caption('Citadels')

def top_deck(card):
    card.set_pos(50, 300)
    card.scale(50, 75)
    v = (8, -7)
    scaling = (20, 30)
    while card.get_rect().w < 300 and card.get_rect().h < 450:
        #print(card.rect.w, card.rect.h)
        card.move(v)
        card.scale_d(scaling)
        refresh_scene(card)
    card.reset_img()


gs = init_game()

def init_view(gs):
    drawable = []
    updatable = []
    clickable = []

    player_hand = PlayerHand(gs.human_player().hand)
    drawable.append(player_hand)
    updatable.append(player_hand)

    deck = Deck(gs.deck)
    drawable.append(deck)
    clickable.append(deck)

    return(drawable, updatable, clickable)



while 1:
    (drawable, updatable, clickable) = init_view(gs)

    for obj in updatable:
        obj.update(pygame.mouse.get_pos())

    refresh_scene(drawable)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mp = pygame.mouse.get_pos()
            for obj in clickable:
                if obj.rect.collidepoint(mp):
                    obj.on_click(gs, mp, drawable)


