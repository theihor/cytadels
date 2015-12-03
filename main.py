#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from game_init import init_game
from view import *
from refresh import refresh_scene
import game
import log
import animation
from characters import CHARACTERS

pygame.init()
log.init_log()
# create window
pygame.display.set_caption('Citadels')
gs = init_game()


def get_view(gs):
    objects = []

    background = Drawable(BACKGROUND_IMAGE)
    objects.append(background)

    for i in range(COUNT_OF_PLAYERS - 1):
        p = gs.players[i+1]
        frame = AIPlayerFrame(p, i, p.role == gs.killed)
        objects.append(frame)
        for slot in frame.slots:
            objects.append(slot)
            if slot.card:
                objects.append(slot.card)

    p = gs.human_player()
    frame = HumanPlayerFrame(p, p.role == gs.killed)
    objects.append(frame)
    for slot in frame.slots:
        objects.append(slot)
        if slot.card:
            objects.append(slot.card)

    player_hand = PlayerHand(gs.human_player().hand)
    objects.append(player_hand)
    objects += player_hand.cards

    deck = Deck(gs.deck)
    objects.append(deck)

    return objects


game.init_round(gs)

objects = get_view(gs)

while not gs.end():
    for obj in [obj for obj in objects if isinstance(obj, Updatable)]:
        mp = pygame.mouse.get_pos()
        if obj.collides(mp):
            obj.on_mouse_over()
        else:
            obj.on_mouse_out()


    refresh_scene(objects)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mp = pygame.mouse.get_pos()
            for obj in [obj for obj in objects if isinstance(obj, Clickable)]:
                if obj.rect.collidepoint(mp):
                    obj.on_click(gs, objects)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
            if gs.current_player < len(CHARACTERS):
                game.next_turn(gs, objects)
            else:
                game.init_round(gs)

