#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from game_init import init_game
from view import *
from refresh import refresh_scene
import game
from actions import *
from characters import CHARACTERS

pygame.init()
init_log()
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
    scene['portraits'] = []
    for i in range(COUNT_OF_PLAYERS - 1):
        p = gs.players[i+1]
        frame = AIPlayerFrame(p, i, p.role == gs.killed, gs.is_crown_owner(p))
        scene['frames'].append(frame)
        for slot in frame.slots:
            scene['slots'].append(slot)
            if slot.card:
                scene['slot_cards'].append(slot.card)
        scene['portraits'].append(frame.portrait)

    p = gs.human_player()
    frame = HumanPlayerFrame(p, p.role == gs.killed, gs.is_crown_owner(p))
    scene['frames'].append(frame)
    scene['portraits'].append(frame.portrait)
    scene['human_player_frame_slots'] = []
    scene['human_player_frame_slot_cards'] = []
    for slot in frame.slots:
        scene['human_player_frame_slots'].append(slot)
        if slot.card:
            scene['human_player_frame_slot_cards'].append(slot.card)

    button = AbilityButton()
    (x, y) = frame.ability_button_pos(button.rect)
    button.set_pos(x, y)
    scene['button'] = [button]

    player_hand = PlayerHand(gs.human_player().hand)
    scene['player_hand'] = [player_hand]
    scene['player_hand_cards'] = player_hand.cards

    deck = Deck(gs.deck)
    scene['deck'] = [deck]

    coins = Coins()
    scene['coins'] = [coins]

    return scene




#scene = get_view(gs)
#objects = scene_objects(scene)

scene = get_view(gs)
objects = scene_objects(scene)
refresh_scene(objects)
game.init_round(gs, scene)
update_roles(scene)

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
        # if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
        #         if gs.current_player < len(CHARACTERS):
        #             if gs.human_turn():
        #                 game.next_turn(gs, scene)
        #         else:
        #             game.init_round(gs, scene)

    clock.tick(GLOBAL_FPS * 0.5)
    if gs.current_player < len(CHARACTERS):
        game.next_turn(gs, scene)
    else:
        game.init_round(gs, scene)
        update_roles(scene)
        #scene = get_view(gs)
        #objects = scene_objects(scene)


