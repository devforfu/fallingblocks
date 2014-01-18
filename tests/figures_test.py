import unittest
import os
import time
import pygame

import graphics
import config
import figures
import game

os.chdir('..')


class BlockCreatorTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 200))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))

    def test_create_block(self):
        blocks = [
            figures.BlockCreator.create_block('amazing_yellow_medium', 255, (1, 1)),
            figures.BlockCreator.create_block('amazing_red_medium', 255, (3, 2))
        ]

        group = pygame.sprite.Group()
        for block in blocks:
            group.add(block)
        stop = False

        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
            self.screen.blit(self.background, (0, 0))
            group.draw(self.screen)
            pygame.display.update()

    def test_figures_creation(self):
        plank = figures.PlankFigure((4, 2), 'amazing_red_medium')
        square = figures.SquareFigure((8, 2), 'amazing_green_medium')
        tfig = figures.TFigure((12, 2), 'amazing_yellow_medium')
        lfig = figures.LFigure((18, 2), 'amazing_yellow_medium')
        zfig = figures.ZFigure((22, 2), 'amazing_red_medium')

        group = pygame.sprite.RenderUpdates()
        group.add(plank)
        group.add(square)
        group.add(tfig)
        group.add(lfig)
        group.add(zfig)

        stop = False

        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
            self.screen.blit(self.background, (0, 0))
            group.draw(self.screen)
            group.update()
            pygame.display.update()

    def test_collisions(self):
        one = figures.PlankFigure((4, 2), 'pixel_yellow_medium')
        two = figures.PlankFigure((8, 2), 'pixel_purple_medium')

        print(pygame.sprite.groupcollide(one, two, False, False))



if __name__ == "__main__":
    unittest.main()
