""" Contains variables and parameters needed by application
    DEF_RES - default screen resolution
"""
from pygame.locals import *


class Screen:
    BOARD_COLS = 10
    BOARD_ROWS = 20

    PIXEL_BLOCK_SIZE = 32
    PIXEL_BOARD_WIDTH = PIXEL_BLOCK_SIZE * BOARD_COLS
    PIXEL_BOARD_HEIGHT = PIXEL_BLOCK_SIZE * BOARD_ROWS

    PIXEL_INFO_WIDTH = PIXEL_BLOCK_SIZE * 6
    PIXEL_INFO_HEIGHT = PIXEL_BOARD_HEIGHT

    BOARD_RECT = Rect((0, 0, PIXEL_BOARD_WIDTH, PIXEL_BOARD_HEIGHT))
    INFO_RECT = Rect((PIXEL_BOARD_WIDTH+1, 0, PIXEL_INFO_WIDTH, PIXEL_BOARD_HEIGHT))
    SCREEN_RECT = Rect((0, 0, PIXEL_BOARD_WIDTH + PIXEL_INFO_WIDTH, PIXEL_BOARD_HEIGHT))


class Menu:
    MENU_WIDTH = 640
    MENU_HEIGHT = 480
    MENU_SIZE = (MENU_WIDTH, MENU_HEIGHT)

    BTN_WIDTH = 200
    BTN_HEIGHT = 40
    BTN_SIZE = (BTN_WIDTH, BTN_HEIGHT)


class Path:
    FONT_DEFAULT = 'fonts/pixel.ttf'


class Color:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREED = (0, 255, 0)
    BLUE = (0, 0, 255)
    DARK_BLUE = (42, 82, 190)
    LIGHT_BLUE = (127, 199, 255)
    WHITE = (255, 255, 255)