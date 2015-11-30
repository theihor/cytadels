from definitions import *
from animation import *
from globalvars import *
from loadimg import *
from view import *


def action_rob(gs, drawable):
    robbed = next(p for p in gs.players if p.role == gs.robbed)
    robber = gs.robber()
    frames = [d for d in drawable if isinstance(d, PlayerFrame) or isinstance(d, HumanPlayerFrame)]
    robbed_frame = next(f for f in frames if f.player.role == robbed.role)
    robber_frame = next(f for f in frames if f.player.role == robber.role)
    (x1, y1) = robbed_frame.global_money_icon_pos()
    (x2, y2) = robber_frame.global_money_icon_pos()
    obj = GameObject(image=MONEY_ICON)
    obj.set_pos(x1, y1)

    m = robbed.money
    robbed.money = 0
    move_animation(obj, (x2, y2), ROBBING_TIME, drawable)
    robber.money += m

