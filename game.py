import sys

import pygame
from pygame.locals import *

import figures
import graphics
from config import Screen, Color, Path


class Game:
    FRAME_NUMBER = 0

    def __init__(self, style: str):
        self.screen = pygame.display.set_mode(Screen.SCREEN_RECT.bottomright, DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.fallen_blocks = pygame.sprite.Group() # contains already fallen blocks
        self.active_figure = None # figure which is currently manipulated by player
        self.next_figure = None
        self.style = style
        self.score = 0
        self.ended, self.isWin, self.isLose = False, False, False

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
            figures.PlankFigure,
            figures.SquareFigure,
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
        import proto

        isRemoved = True
        count = 0

        while isRemoved:
            isRemoved = False
            for y in range(Screen.BOARD_ROWS, 0, -1):
                blocks = [b for b in self.fallen_blocks if b.get_y() == y]
                if len(blocks) == Screen.BOARD_COLS:
                    upper_blocks = [b for b in self.fallen_blocks if b.get_y() < y]
                    for b in upper_blocks:
                        b.move_block_down()
                    for b in blocks:
                        b.kill()
                    isRemoved = True
                    count += 1
                    break

        self.score += 100 * count * count

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
        """ Includes drawing of sky, border, crane and background for info"""
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
        image = pygame.transform.scale(image, Screen.INFO_RECT.size)
        image.set_alpha(120)
        screen.blit(image, (Screen.PIXEL_BOARD_WIDTH, 0))

    def draw_fonts(self):
        font = pygame.font.Font(Path.FONT_DEFAULT, 32)
        self.screen.blit(font.render('next', False, Color.DARK_BLUE), (357, 320))
        # game score
        self.screen.blit(font.render('score', False, Color.DARK_BLUE), (340, 50))
        score = str(self.score)
        n = len(score)
        if n < 5:
            score = '0' * (5-n) + score
        self.screen.blit(font.render(score, False, Color.DARK_BLUE), (340, 90))

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
        figure = self.next_figure.copy_to((Screen.BOARD_COLS + 3, Screen.BOARD_ROWS - 7))
        x = Screen.PIXEL_BLOCK_SIZE * (Screen.BOARD_COLS + 1)
        y = Screen.PIXEL_BLOCK_SIZE * (Screen.BOARD_ROWS - 9)
        w = h = Screen.PIXEL_BLOCK_SIZE * 4
        self.screen.fill(
            (22, 22, 22),
            Rect(x, y, w, h),
            BLEND_ADD
        )
        figure.draw(self.screen)

    def init_figures(self):
        self.active_figure = self.random_figure()
        self.next_figure = self.random_figure()
        self.active_figure.set_game_ref(self)

    def reset(self):
        self.fallen_blocks = pygame.sprite.Group()
        self.active_figure, self.next_figure = None, None
        self.ended, self.isWin, self.isLose = False, False, False

    def mainloop(self):
        """ Game event loop. Returns boolean value when game is ended.
            If player chooses 'New game' then it function returns
            True, else - returns False.
        """
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
            self.draw_fonts()
            # game board grid drawing
            self.draw_grid()
            # draw controlled by player figure and already fallen blocks
            self.active_figure.draw(screen)
            self.fallen_blocks.draw(screen)
            self.draw_next_figure()

            for event in pygame.event.get(): # dispatch game event
                if event.type == QUIT:
                    sys.exit(0)

                elif not self.ended: # keyboard polling if game is not ended
                    if event.type == KEYDOWN:
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

                elif self.ended:  # if game ended then exit
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return False
                        else:
                            return True

            if self.isWin:  # player won
                pass

            elif self.isLose:  # player lose
                self.game_over()
                self.active_figure.update()
                self.fallen_blocks.update()

            else:  # game is going
                if not Game.FRAME_NUMBER % slowdownRate:
                    self.active_figure.move_down()
                    if self.active_figure.is_landed():
                        # if new figure cannot move down then game is over
                        if self.active_figure.get_center()[1] == 1:
                            self.ended = True
                            self.isLose = True
                        else:
                            self.fallen_blocks.add(self.active_figure.sprites())
                            self.active_figure = self.next_figure
                            self.active_figure.set_game_ref(self)
                            self.next_figure = self.random_figure()
                            self.check_rows()
                            slowdownRate = 10  # slow down game speed when figure is landed

            self.active_figure.update()
            self.fallen_blocks.update()
            pygame.display.update()

    def run(self):
        newGame = True
        while newGame:
            self.reset()
            newGame = self.mainloop()
        sys.exit(0)