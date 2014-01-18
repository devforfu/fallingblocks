import sys

import pygame
from pygame.locals import *

import figures
import graphics
from config import Screen, Color


class Game:
    FRAME_NUMBER = 0

    def __init__(self, style: str):
        pygame.init()

        self.screen = pygame.display.set_mode(Screen.SCREEN_RECT.bottomright, DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.fallen_blocks = pygame.sprite.Group() # contains already fallen blocks
        self.active_figure = None # figure which is currently manipulated by player
        self.next_figure = None
        self.style = style

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

    def get_fallen_blocks(self):
        """ Returns list containing already fallen blocks sprites """
        return self.fallen_blocks

    def create_figure(self, type: str):
        pass

    def random_figure(self):
        """ Returns fihure with random type and position """
        import random
        types = [
            figures.PlankFigure,
            figures.SquareFigure,
            figures.LFigure,
            figures.TFigure,
            figures.ZFigure,
            figures.LMirrorFigure,
            figures.ZMirrorFigure
        ]
        Figure = random.choice(types)
        styles = [k for k, v in figures.BlockCreator.types.items()
                  if k.startswith(self.style)]
        return Figure((random.randint(2, Screen.BOARD_COLS - 2), 1),
                      random.choice(styles))

    def check_rows(self):
        """ This function checks game board to find complete row. It is called after
            landing of active figure. If there are some complete rows on game board
            these rows will be removed from screen. The blocks which were placed on
            the top of removed rows will be shifted.
        """
        from itertools import groupby
        from operator import itemgetter

        # collecting block's coordinates
        y_coords = sorted([block.get_y() for block in self.fallen_blocks])
        # group equal coordinates together
        y_coords = [list(g) for k, g in groupby(y_coords)]
        # take coordinates of complete rows
        y_coords = list(map(itemgetter(0),
                            (filter(lambda x: len(x) == Screen.BOARD_COLS, y_coords))))
        y_coords.sort()

        if y_coords: # if there are some complete rows
            removing_blocks = [block for block in self.fallen_blocks if block.get_y() in y_coords]
            fringe_blocks = [block for block in self.fallen_blocks if block.get_y() < y_coords[0]]
            bottom_blocks = [block for block in self.fallen_blocks if block.get_y() > y_coords[-1]]

            self.fallen_blocks.remove(removing_blocks) # then remove them

            while True: # and move other blocks on the appropriate distance
                for block in fringe_blocks:
                    block.move_block_down()
                collided = pygame.sprite.groupcollide
                if collided(fringe_blocks, bottom_blocks, False, False) \
                    or any([b.get_y() == 20 for b in fringe_blocks]):
                    for block in fringe_blocks:
                        block.move_block_up()
                    break

    def game_over(self):
        image, rect = graphics.load_image('gameover_bg32.png')
        image = pygame.transform.scale(image, Screen.SCREEN_RECT.size)
        image.set_alpha(150)
        self.screen.blit(image, (0, 0))

        image, rect = graphics.load_image('gameover_text.png', (255, 255, 255))
        rc = Screen.SCREEN_RECT
        shifted = rc.center[0] - rect.width / 2, rc.center[1] - rect.height / 2
        self.screen.blit(image, shifted)

    def draw_background(self):
        screen = self.screen
        # draw ground and sky
        image, rect = graphics.load_image('back.png')
        image.set_alpha(200)
        for x in range(0, Screen.SCREEN_RECT.width, rect.width):
            screen.blit(image, (x, 0))
        # draw builder crane
        image, rect = graphics.load_image('tap.png')
        image.set_colorkey(image.get_at((1,1)))
        screen.blit(image, (100, Screen.SCREEN_RECT.height - 128 - rect.height))
        # draw fence
        image, rect = graphics.load_image('border.png', (255, 255, 255))
        image.set_alpha(200)
        for x in range(0, Screen.SCREEN_RECT.width, rect.width):
            screen.blit(image, (x, 0))
        # draw transparent blue rect (game info will be placed over it)
        image, rect = graphics.load_image('info_bg32.png')
        image = pygame.transform.scale(image, Screen.SCREEN_RECT.size)
        image.set_alpha(120)
        self.screen.blit(image, (Screen.PIXEL_BOARD_WIDTH, 0))

    def draw_grid(self):
        """ Function draws rectangular grid on the game board """
        step = Screen.PIXEL_BLOCK_SIZE
        width = Screen.PIXEL_BOARD_WIDTH
        height = Screen.PIXEL_BOARD_HEIGHT

        for y in range(0, height + step, step):
            pygame.draw.line(self.screen, (87, 87, 87), (0, y), (width, y), 1)
        for x in range(0, width + step, step):
            pygame.draw.line(self.screen, (87, 87, 87), (x, 0), (x, height), 1)

    def draw_next_figure(self):
        figure = self.next_figure.copy_to((15, 15))
        figure.draw(self.screen)

    def init_figures(self):
        self.active_figure = self.random_figure()
        self.next_figure = self.random_figure()
        self.active_figure.set_game_ref(self)

    def mainloop(self):
        self.init_figures()
        screen, background = self.screen, self.background

        slowdownRate = 10
        speedUp = False

        while True:
            self.clock.tick(30)
            Game.FRAME_NUMBER += 1
            # background drawing
            screen.blit(background, (0, 0))
            self.draw_background()

            font = pygame.font.Font('fonts/pixel.ttf', 48)
            # screen.blit(font.render('01234', False, Color.BLACK), (350, 400))

            # game board grid drawing
            self.draw_grid()
            # draw controlled by player figure and already fallen blocks
            self.active_figure.draw(screen)
            self.fallen_blocks.draw(screen)
            self.draw_next_figure()

            for event in pygame.event.get(): # dispatch game event
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    k = event.key
                    if k == K_ESCAPE:
                        sys.exit(0)
                    elif k == K_LEFT:
                        self.active_figure.move_left()
                    elif k == K_RIGHT:
                        self.active_figure.move_right()
                    elif k == K_DOWN:
                        self.active_figure.rotate_counterclockwise()
                    elif k == K_UP:
                        self.active_figure.rotate_clockwise()
                    elif k == K_SPACE:
                        # speed up figure moving
                        slowdownRate = 1

            if not Game.FRAME_NUMBER % slowdownRate:
                self.active_figure.move_down()
                if self.active_figure.is_landed():
                    if self.active_figure.get_center()[1] == 1:
                        self.game_over()
                        self.active_figure.update()
                        self.fallen_blocks.update()
                        pygame.display.update()
                        input('Press any key...')
                        sys.exit(0)

                    self.fallen_blocks.add(self.active_figure.sprites())
                    self.active_figure = self.next_figure
                    self.active_figure.set_game_ref(self)
                    self.next_figure = self.random_figure()
                    self.check_rows()
                    slowdownRate = 10 # slow down game speed when figure is landed

            self.active_figure.update()
            self.fallen_blocks.update()
            pygame.display.update()
