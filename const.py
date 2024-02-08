import pygame
import os

pygame.init()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Не удаётся загрузить:', name)
        return False
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


WHITE = 1
BLACK = 0

instability = 5

size = width, height = 800, 800
cell_size = 100
left = 0
top = 0

FPS = 50
clock = pygame.time.Clock()
time = -1
