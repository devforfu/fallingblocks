import pygame
import game


def main():
    if not pygame.font:
        print('Warning: fonts disabled')
    if not pygame.mixer:
        print('Warning: sound disabled')
    game.Game('pixel').mainloop()


if __name__ == '__main__':
    main()