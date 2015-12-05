from definitions import *
from animation import *
from globalvars import *
from view import *
import pygame

def action_rob(gs, scene):
    objects = []
    for key in scene:
        objects += scene[key]

    robbed = next(p for p in gs.players if p.role == gs.robbed)
    robber = gs.robber()
    frames = scene['frames']
    robbed_frame = next(f for f in frames if f.player.role == robbed.role)
    robber_frame = next(f for f in frames if f.player.role == robber.role)
    (x1, y1) = robbed_frame.global_money_icon_pos()
    (x2, y2) = robber_frame.global_money_icon_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x1, y1)

    m = robbed.money
    robbed.money = 0
    move_animation(obj, (x2, y2), ROBBING_TIME, objects)
    robber.money += m


def action_build(scene, p, card_dict):
    objects = scene_objects(scene)
    card = card_from_dict(card_dict)

    frame = next(f for f in scene['frames'] if f.player == p)

    # spend money
    (x, y) = frame.global_money_icon_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x, y)
    p.money -= card_dict['price']
    move_with_a_animation(obj, (x, -obj.size()[1]), 0.4, objects)

    # play card
    p.hand.remove(card_dict)
    if isinstance(frame, HumanPlayerFrame):
        scene['player_hand'] = [PlayerHand(p.hand)]
        scene['player_hand_cards'] = scene['player_hand'][0].cards
    slot = frame.next_slot()

    (x, y) = frame.global_cards_icon_pos()
    (w, h) = CARDS_ICON.get_rect().size
    card.set_pos(x, y)
    card.scale(w, h)
    open_card_animation(card, slot.card_pos(), slot.card_size(), drawable=objects)

    # set card in slot
    p.slots.append(card_dict)
    frame.put_card_in_slots(card, scene)

    log(p.roled_name() + ' builds ' + str_card(card_dict) + ' and now has ' + str(p.base_score()) + ' Score')


def action_reveal(scene, p):
    objects = scene_objects(scene)
    frame = next(f for f in scene['frames'] if f.player == p)
    p.revealed = True

    card = frame.portrait
    card.init_img()
    frame.adjust_portrait()
    objects.remove(card)

    open_card_animation(card, card.pos(), card.size(), drawable=objects)


def action_player_chooses_role(role_names, gs, scene):
    role_names.sort(key=lambda x: CHARACTERS_N[x])

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    cards = []
    for name in role_names:
        card = Drawable(image=CHARACTER_IMAGES[name], size=CARD_SIZE_CHOICE)
        card.set_pos(600, 400)
        card.draw_priority = -1
        cards.append(card)

    choosing_start_animation(cards, objects)



