from globalvars import *
import pygame

clock = pygame.time.Clock()
window = pygame.display.set_mode(WINDOW_SIZE)


def refresh_scene(drawable=[]):
    clock.tick(GLOBAL_FPS)
    window.fill(COLOR_WHITE)

    drawable.sort(key=lambda x: x.draw_priority, reverse=True)
    for obj in drawable:
        obj.draw(window)

    pygame.display.flip()
    pass
