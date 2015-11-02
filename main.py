#!/usr/bin/python3
import pygame
import sys
from globalvars import *
from card import *
from game_init import init_game
from view import *

pygame.init()

# create window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Citadels')


#the_card = NoImgCard(50, 300, "Test", 5, 6, 5)
#the_card.scale(50, 75)
clock = pygame.time.Clock()


def refresh_scene(gs, mouse_pos=None):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)
    draw_game_state(window, gs, mouse_pos)
    pygame.display.flip()
    pass


def show_card(card):
    window.blit(card.img, card.pos)


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
    player_hand = PlayerHand(gs.human_player().hand)
    drawable.append(player_hand)
    updatable.append(player_hand)
    deck = Deck(gs.deck)
    drawable.append(deck)
    return(drawable, updatable)



while 1:
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)

    (drawable, updatable) = init_view(gs)

    for obj in updatable:
        obj.update(pygame.mouse.get_pos())
    for obj in drawable:
        obj.draw(window)

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        # if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        #     print(pygame.mouse.get_pos())
        #     print(the_card.get_rect())
        #     if the_card.get_rect().collidepoint(pygame.mouse.get_pos()):
        #         top_deck(the_card)


