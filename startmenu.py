import sys
import os

import pygame
from pygame.locals import *

from config import Screen, Color, Path
import figures
import game
import graphics

class StartMenu:
    class State:
        Main = 1
        GameLoop = 2
        Controls = 3

    global_state = State.Main

    def __init__(self, size, btn_size, font_size):
        self.screen = pygame.display.set_mode(size, DOUBLEBUF)

        self.current = 1
        self.options = ['resume', 'start', 'controls', 'exit']
        self.resume_disabled = True

        self.width, self.height = self.size = size
        self.center = self.width / 2, self.height / 2
        self.btn_w, self.btn_h = self.btn_size = btn_size
        self.font_size = font_size

        self.opts = {
            K_ESCAPE: self.exit,
            K_SPACE: self.submit,
            K_RETURN: self.submit,
            K_UP: self.prev_button,
            K_DOWN: self.next_button
        }

        self.current_painter = self.main_painter

        self.load_screen()
        self.draw_screen()


    def load_screen(self):
        self.font = pygame.font.Font(Path.FONT_DEFAULT, self.font_size)

    # ------- Game menu options -------
    def start(self):
        StartMenu.global_state = StartMenu.State.GameLoop
        self.current_painter = self.game_painter

    def exit(self):
        sys.exit(0)

    def resume(self):
        pass

    def controls(self):
        StartMenu.global_state = StartMenu.State.Controls
        self.current_painter = self.controls_painter
        self.screen.fill(Color.LIGHT_BLUE)
    # ---------------------------------

    # -- Navigation between buttons ---
    def submit(self):
        {
            0: self.resume,
            1: self.start,
            2: self.controls,
            3: self.exit
        }[self.current]()

    def next_button(self):
        if self.current == len(self.options) - 1:
            if self.resume_disabled:
                self.current = 1
            else:
                self.current = 0
        else:
            self.current += 1

    def prev_button(self):
        print(self.current == 1 and self.resume_disabled)
        if self.current == 0 or (self.current == 1 and self.resume_disabled):
            self.current = len(self.options) - 1
        else:
            self.current -= 1
    # ---------------------------------

    # ----------- Painters ------------
    def main_painter(self):
        xCenter, yCenter = self.center
        btnLeft, btnTop  = xCenter - self.btn_w / 2, yCenter - self.btn_h / 2
        btnRect = pygame.Rect((btnLeft, btnTop) + self.btn_size)
        btnRect = btnRect.move(0, -40)

        self.screen.fill(Color.WHITE, btnRect)

        oldPos = btnRect.topleft

        for i, opt in enumerate(self.options):
            if not i and self.resume_disabled:
                continue
            rc = btnRect.copy()
            rc.height = 40
            if i == self.current:
                self.screen.fill(Color.WHITE, rc)
            else:
                self.screen.fill(Color.LIGHT_BLUE, rc)
            fontPos = btnRect.left + 10, btnRect.top + btnRect.height / 3
            self.screen.blit(self.font.render(opt, True, Color.DARK_BLUE), fontPos)
            btnRect.y += 40

        btnRect.topleft = oldPos

    def controls_painter(self):
        upArrow, _ = graphics.load_image('keys/up.png')
        self.screen.blit(upArrow, (100, 100))

    def game_painter(self):
        game.Game('pixel').run()
    # ----------------------------------------------

    def draw_screen(self):
        self.screen.fill(Color.LIGHT_BLUE)

        while True:
            #if self.global_state == StartMenu.State.Main:
            self.current_painter()

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key in self.opts:
                    if StartMenu.global_state == StartMenu.State.Controls:
                        StartMenu.global_state = StartMenu.State.Main
                        self.current_painter = self.main_painter
                        self.screen.fill(Color.LIGHT_BLUE)

                    elif StartMenu.global_state == StartMenu.State.GameLoop:
                        StartMenu.global_state = StartMenu.State.Main
                        self.current_painter = self.main_painter
                        self.screen.fill(Color.LIGHT_BLUE)

                    else:
                        self.opts[event.key]()

            pygame.display.update()

