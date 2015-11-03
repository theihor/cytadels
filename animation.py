from refresh import *


def delay_animation(obj, time, drawable):
    old_dp = obj.draw_priority
    obj.draw_priority = 0
    ticks = round(time * GLOBAL_FPS)
    drawable.append(obj)
    for t in range(ticks):
        refresh_scene(drawable)
    obj.draw_priority = old_dp


def move_and_scale_animation(obj, new_pos, new_size, time, drawable):
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
