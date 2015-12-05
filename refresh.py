from globalvars import *
from gameobject import Drawable
import pygame

clock = pygame.time.Clock()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.font.init()


def refresh_scene(objects):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)

    objects = [obj for obj in objects if isinstance(obj, Drawable)]
    objects.sort(key=lambda x: x.draw_priority, reverse=True)
    for obj in objects:
        obj.draw(window)

    pygame.display.flip()
    pass

