import os
import pygame
from pygame.locals import *


def load_image(name, color_key=None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as msg:
        print('Cannot load image: ', name)
        raise SystemExit(msg)
    image = image.convert()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('sound', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as msg:
        print('Cannot load sound')
        raise SystemExit(msg)
    return sound