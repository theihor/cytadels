from gameobject import *
from loadimg import *


def refresh_scene(objects):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)

    objects = [obj for obj in objects if isinstance(obj, Drawable)]
    objects.sort(key=lambda x: x.draw_priority, reverse=True)
    for obj in objects:
        obj.draw(window)

    pygame.display.flip()
    pass

