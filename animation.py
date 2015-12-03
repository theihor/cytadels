from refresh import *
from globalvars import *
from gameobject import *
from math import hypot
from loadimg import *

def get_cardback():
    return Drawable(CARD_BACK_IMAGE)


def delay_animation(obj, time, drawable=DRAWABLE):
    old_dp = obj.draw_priority
    obj.draw_priority = 0
    ticks = round(time * GLOBAL_FPS)
    drawable.append(obj)
    for t in range(ticks):
        refresh_scene(drawable)
    obj.draw_priority = old_dp


def move_animation(obj, new_pos, time, drawable=DRAWABLE):
    old_dp = obj.draw_priority
    obj.draw_priority = 0
    ticks = round(time * GLOBAL_FPS)
    (x1, y1) = obj.pos()
    (x2, y2) = new_pos
    (vx, vy) = ((x2 - x1) / ticks, (y2 - y1) / ticks)
    drawable.append(obj)
    (x, y) = (x1, y1)

    for t in range(ticks):
        obj.set_pos(round(x), round(y))
        refresh_scene(drawable)
        (x, y) = (x + vx, y + vy)
    obj.set_pos(x2, y2)
    refresh_scene(drawable)
    obj.draw_priority = old_dp
    drawable.remove(obj)


def move_with_a_animation(obj, new_pos, time, drawable=DRAWABLE):
    old_dp = obj.draw_priority
    obj.draw_priority = 0
    ticks = round(time * GLOBAL_FPS)
    (x1, y1) = obj.pos()
    (x2, y2) = new_pos
    (vx, vy) = (0, 0)
    ax = (x2 - x1) * 2 / (ticks ** 2)
    ay = (y2 - y1) * 2 / (ticks ** 2)
    drawable.append(obj)
    (x, y) = (x1, y1)

    for t in range(ticks):
        obj.set_pos(round(x), round(y))
        refresh_scene(drawable)
        (vx, vy) = (vx + ax, vy + ay)
        (x, y) = (x + vx, y + vy)
    obj.set_pos(x2, y2)
    refresh_scene(drawable)
    obj.draw_priority = old_dp
    drawable.remove(obj)


def move_and_scale_animation(obj, new_pos, new_size, time, drawable=DRAWABLE):
    old_dp = obj.draw_priority
    obj.draw_priority = 0
    ticks = round(time * GLOBAL_FPS)
    (x1, y1) = obj.rect.topleft
    (w1, h1) = obj.rect.size
    (x2, y2) = new_pos
    (w2, h2) = new_size
    (vx, vy) = ((x2 - x1) / ticks, (y2 - y1) / ticks)
    (dw, dh) = ((w2 - w1) / ticks, (h2 - h1) / ticks)
    drawable.append(obj)
    (x, y) = (x1, y1)
    (w, h) = (w1, h1)
    for t in range(ticks):
        obj.set_pos(round(x), round(y))
        obj.scale(round(w), round(h))
        refresh_scene(drawable)
        (x, y) = (x + vx, y + vy)
        (w, h) = (w + dw, h + dh)
    obj.scale(w2, h2)
    obj.set_pos(x2, y2)
    refresh_scene(drawable)
    obj.draw_priority = old_dp
    drawable.remove(obj)


def show_message(s, time=0.7, drawable=DRAWABLE):
    ticks = round(time * GLOBAL_FPS)
    (w, h) = WINDOW_SIZE
    f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, w // 20)
    text = f.render(s, 1, COLOR_WHITE, COLOR_BLACK)
    obj = Drawable(image=text)
    obj.set_pos((w - text.get_rect().w) // 2, (h - text.get_rect().h) // 2)
    drawable.append(obj)
    obj.draw_priority = 0
    for t in range(ticks):
        refresh_scene(drawable)
    drawable.remove(obj)


def open_card_animation(obj, new_pos, new_size, opened_pos=SHOW_CARD_POS, time=1, drawable=DRAWABLE):
    (x, y) = DECK_POSITION
    (w, h) = CARD_SIZE_DECK
    obj.scale(w, h)
    obj.set_pos(x, y)
    (dest_x, dest_y) = SHOW_CARD_POS
    cardback = get_cardback()
    cardback.scale(w, h)
    cardback.set_pos(x, y)
    move_and_scale_animation(cardback, (x + w // 2, y), (0, h), 0.2, drawable)
    obj.set_rect((x + w // 2, y), (0, h))
    move_and_scale_animation(card, (x, y), (w, h), 0.2, drawable)

    move_and_scale_animation(card, (dest_x, dest_y), CARD_SIZE_DEFAULT, 0.4, drawable)
    delay_animation(card, 0.6, drawable)
    move_and_scale_animation(card, hand_pos, CARD_SIZE_HAND, 0.3, drawable)
    pass


def choice_pos(i, n):
    if n <= 3:
        return i

def choosing(choosable, drawable):
    n = len(choosable)

