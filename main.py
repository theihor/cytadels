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
    scene = {}

    background = Drawable(BACKGROUND_IMAGE)
    scene['background'] = [background]

    scene['frames'] = []
    scene['slots'] = []
    scene['slot_cards'] = []
    for i in range(COUNT_OF_PLAYERS - 1):
        p = gs.players[i+1]
        frame = AIPlayerFrame(p, i, p.role == gs.killed)
        scene['frames'].append(frame)
        for slot in frame.slots:
            scene['slots'].append(slot)
            if slot.card:
                scene['slot_cards'].append(slot.card)

    p = gs.human_player()
    frame = HumanPlayerFrame(p, p.role == gs.killed)
    scene['frames'].append(frame)
    scene['human_player_frame_slots'] = []
    scene['human_player_frame_slot_cards'] = []
    for slot in frame.slots:
        scene['human_player_frame_slots'].append(slot)
        if slot.card:
            scene['human_player_frame_slot_cards'].append(slot.card)

    player_hand = PlayerHand(gs.human_player().hand)
    scene['player_hand'] = [player_hand]
    scene['player_hand_cards'] = player_hand.cards

    deck = Deck(gs.deck)
    scene['deck'] = [deck]

    return scene


game.init_round(gs)

scene = get_view(gs)
objects = scene_objects(scene)
while not gs.end():
    objects = scene_objects(scene)
    for obj in [obj for obj in objects if isinstance(obj, Updatable)]:
        mp = pygame.mouse.get_pos()
        if obj.collides(mp):
            obj.on_mouse_over()
        else:
            obj.on_mouse_out()
        pass
    refresh_scene(objects)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mp = pygame.mouse.get_pos()
            for obj in [obj for obj in objects if isinstance(obj, Clickable)]:
                if obj.rect.collidepoint(mp):
                    obj.on_click(gs, objects)
        #if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:

    clock.tick(GLOBAL_FPS * 0.2)
    if gs.current_player < len(CHARACTERS):
        game.next_turn(gs, scene)
    else:
        game.init_round(gs)

