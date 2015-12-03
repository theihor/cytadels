from definitions import *
from animation import *
from globalvars import *
from loadimg import *
from view import *


def action_rob(gs, scene):
    objects = []
    for key in scene:
        objects += scene[key]

    robbed = next(p for p in gs.players if p.role == gs.robbed)
    robber = gs.robber()
    #frames = [d for d in drawable if isinstance(d, PlayerFrame) or isinstance(d, HumanPlayerFrame)]
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


def action_build(scene, p, card):
    objects = []
    for key in scene:
        objects += scene[key]
    frame = next(f for f in scene['frames'] if f.player == p)

    # spend money
    (x, y) = frame.global_money_icon_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x, y)
    p.money -= card['price']
    move_with_a_animation(obj, (x, -obj.size()[1]), 0.4, objects)

    # play card
    p.hand.remove(card)

    # set card in slot
    p.slots.append(card)
    frame.put_card_in_slots(card, scene)

    log(p.roled_name() + ' builds ' + str_card(card) + ' and now has ' + str(p.base_score()) + ' Score')
