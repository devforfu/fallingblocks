import pygame
import game
import startmenu


def main():
    if not pygame.font:
        print('Warning: fonts disabled')
    if not pygame.mixer:
        print('Warning: sound disabled')

    pygame.init()
    startmenu.StartMenu((640, 480), (200, 40), 20).show()
    game.Game('pixel').run()


if __name__ == '__main__':
    main()