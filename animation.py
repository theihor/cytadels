from gameobject import *
from math import hypot
from loadimg import *
from refresh import *


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


def move_with_a_animation(obj, new_pos, time=0.4, drawable=DRAWABLE):
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


def move_and_scale_animation(obj, new_pos, new_size, time=0.4, drawable=DRAWABLE):
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


def open_card_animation(obj, new_pos, new_size, opened_pos=SHOW_CARD_POS, t=1, drawable=DRAWABLE):
    (x, y) = obj.pos()
    (w, h) = obj.size()
    cardback = get_cardback()
    cardback.scale(w, h)
    cardback.set_pos(x, y)
    (ox, oy) = opened_pos
    (ow, oh) = CARD_SIZE_DEFAULT

    t1, t2 ,t3, t4 = t * 0.1, t * 0.15, t * 0.5, t * 0.25

    move_and_scale_animation(cardback, (x + (ox - x) // 4, y + (oy - y) // 4), (0, oh // 4), t1, drawable)
    obj.set_rect((x + (ox - x) // 4, y + (oy - y) // 4), (0, oh // 4))
    move_and_scale_animation(obj, (ox, oy), CARD_SIZE_DEFAULT, t2, drawable)
    delay_animation(obj, t3, drawable)
    move_and_scale_animation(obj, new_pos, new_size, t4, drawable)
    pass


def move_group_animation(objs_and_poss, time=0.5, drawable=DRAWABLE):
    obj_pos_vs = []
    old_dps = []
    ticks = round(time * GLOBAL_FPS)
    for (obj, new_pos) in objs_and_poss:
        old_dps.append(obj.draw_priority)
        obj.draw_priority = 0
        (x1, y1) = obj.pos()
        (x2, y2) = new_pos
        (vx, vy) = ((x2 - x1) / ticks, (y2 - y1) / ticks)
        drawable.append(obj)
        (x, y) = (x1, y1)
        obj_pos_vs.append((obj, (x, y), (vx, vy)))

    for t in range(ticks):

        for i in range(len(obj_pos_vs)):
            (obj, (x, y), (vx, vy)) = obj_pos_vs[i]
            obj.set_pos(round(x), round(y))
            #print(t)

            obj_pos_vs[i] = (obj, (x + vx, y + vy), (vx, vy))
        refresh_scene(drawable)

    for i in range(len(objs_and_poss)):
        (obj, (x2, y2)) = objs_and_poss[i]
        obj.set_pos(x2, y2)
        refresh_scene(drawable)
        obj.draw_priority = old_dps[i]
        #drawable.remove(obj)


# ops === (object, position, size)
def move_and_scale_group_animation(opss, time=0.5, drawable=DRAWABLE):
    obj_pos_vs_size_ds = []
    old_dps = []
    ticks = round(time * GLOBAL_FPS)
    for (obj, new_pos, new_size) in opss:
        old_dps.append(obj.draw_priority)
        obj.draw_priority = 0
        (x1, y1) = obj.pos()
        (x2, y2) = new_pos
        (vx, vy) = ((x2 - x1) / ticks, (y2 - y1) / ticks)

        (w1, h1) = obj.rect.size
        (w2, h2) = new_size
        (dw, dh) = ((w2 - w1) / ticks, (h2 - h1) / ticks)

        drawable.append(obj)
        (x, y) = (x1, y1)
        (w, h) = (w1, h1)
        obj_pos_vs_size_ds.append((obj, (x, y), (vx, vy), (w, h), (dw, dh)))

    for t in range(ticks):

        for i in range(len(obj_pos_vs_size_ds)):
            (obj, (x, y), (vx, vy), (w, h), (dw, dh)) = obj_pos_vs_size_ds[i]
            obj.set_pos(round(x), round(y))
            obj.scale(round(w), round(h))

            obj_pos_vs_size_ds[i] = (obj, (x + vx, y + vy), (vx, vy), (w + dw, h + dh), (dw, dh))
        refresh_scene(drawable)

    for i in range(len(obj_pos_vs_size_ds)):
        (obj, (x2, y2), (w2, h2)) = opss[i]
        obj.set_pos(x2, y2)
        obj.scale(w2, h2)
        refresh_scene(drawable)
        obj.draw_priority = old_dps[i]


def choice_pos(i, n):
    #print(i, n)
    (w, h) = CARD_SIZE_CHOICE
    (l, m) = WINDOW_SIZE
    if n <= 4:
        b = (l - n * w) // (n + 3)
        a = 2 * b
        x = a + (w + b) * i
        y = (m - h) // 2
        return x, y
    else:
        n2 = n // 2
        n1 = n - n2
        b = h // 8
        a = (m - h * 2 - b) // 2
        if i < n1:
            (x, y) = choice_pos(i, n1)
            y = a
            return x, y
        else:
            (x, y) = choice_pos(i - n1, n2)
            y = a + h + b
            return x, y


def choosing_start_animation(objs, drawable):
    n = len(objs)
    objs_and_poss = []
    for i in range(len(objs)):
        objs_and_poss.append((objs[i], choice_pos(i, n)))
    move_group_animation(objs_and_poss, drawable=drawable)
    #clock.tick(0.5)


def end_round_animation(objs, drawable):
    opss = []
    for obj in objs:
        opss.append((obj, CHOICE_DECK_POSITION, CARD_SIZE_CHOICE))
    move_and_scale_group_animation(opss, drawable=drawable)


