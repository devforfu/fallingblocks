""" dispatcher.py
    Manages game windows.
"""

import pygame
from pygame.locals import *

import figures
import graphics
from config import Screen, Color, Path


class WindowDispatcher:
    current_window = None
    controlled_windows = {}
    FRAME_NUMBER = 0

    def __init__(self):
        #self.screen = pygame.display.set_mode(Screen.SCREEN_RECT.bottomright, DOUBLEBUF)
        #self.clock = pygame.time.Clock()
        pass

    def mainloop(self):
        pass



    def add_window(self, wnd, name, opts={}):
        WindowDispatcher.windows[wnd]