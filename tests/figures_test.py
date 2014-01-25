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

    @unittest.skip('block creation was tested')
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

    @unittest.skip('figures creation was tested')
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
        import collections

        self.screen = pygame.display.set_mode((320, 320))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))

        coords = list(zip([1, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5], [6, 6, 5, 6, 8, 6, 7, 8, 9, 6, 8]))
        coords += list(zip([5, 6, 7, 8, 8, 8, 9], [2, 2, 2, 2, 3, 4, 4]))
        coords += list(zip([8, 8, 8, 9, 9], [6, 8, 9, 8, 9]))
        blocks = []
        group = pygame.sprite.Group()

        stop = False

        for pos in coords:
            block = figures.BlockCreator.create_block('pixel_purple_medium', 255, pos)
            group.add(block)
            blocks.append(block)

        def left(pos):
            x, y = pos
            if x < 1:
                return None
            return x-1, y

        def right(pos):
            x, y = pos
            if x >= 10:
                return None
            return x+1, y

        def up(pos):
            x, y = pos
            if y < 1:
                return None
            return x, y-1

        def down(pos):
            x, y = pos
            if y >= 10:
                return None
            return x, y+1

        connected_components = []
        while coords:
            start, coords = coords[0], coords[1:]
            closed = [start]
            fringe = collections.deque()
            fringe.append(start)

            while fringe:
                u = fringe.popleft()
                neighbors = left(u), right(u), up(u), down(u)
                for pair in neighbors:
                    if pair not in coords:
                        continue
                    if pair is not None and pair not in closed:
                        fringe.append(pair)
                        closed.append(pair)
                        coords.remove(pair)

            connected_components.append(closed)

        for c in connected_components:
            print(c)

        #while not stop:
        #    self.screen.blit(self.background, (0, 0))
        #    group.draw(self.screen)
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            stop = True
        #    pygame.display.update()




if __name__ == "__main__":
    unittest.main()
