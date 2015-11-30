from refresh import *
from globalvars import *
from gameobject import GameObject


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
    print(x1, y1)
    print(x2, y2)

    for t in range(ticks):

        obj.set_pos(round(x), round(y))
        refresh_scene(drawable)
        (x, y) = (x + vx, y + vy)
    obj.set_pos(x2, y2)
    refresh_scene(drawable)
    obj.draw_priority = old_dp


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


def show_message(s, time=0.7, drawable=DRAWABLE):
    ticks = round(time * GLOBAL_FPS)
    (w, h) = WINDOW_SIZE
    f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, w // 20)
    text = f.render(s, 1, COLOR_WHITE, COLOR_BLACK)
    obj = GameObject(image=text)
    obj.set_pos((w - text.get_rect().w) // 2, (h - text.get_rect().h) // 2)
    drawable.append(obj)
    obj.draw_priority = 0
    for t in range(ticks):
        refresh_scene(drawable)
    drawable.remove(obj)


def choice_pos(i, n):
    if n <= 3:
        return i

def choosing(choosable, drawable):
    n = len(choosable)

