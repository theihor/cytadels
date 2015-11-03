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
gs = init_game()

def get_view(gs):
    drawable = []
    updatable = []
    clickable = []

    background = GameObject(BACKGROUND_IMAGE)
    drawable.append(background)

    player_hand = PlayerHand(gs.human_player().hand)
    drawable.append(player_hand)
    updatable.append(player_hand)

    deck = Deck(gs.deck)
    drawable.append(deck)
    clickable.append(deck)

    return(drawable, updatable, clickable)



while 1:
    (drawable, updatable, clickable) = get_view(gs)

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


