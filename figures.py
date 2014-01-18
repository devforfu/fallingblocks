""" Contains classes which implement falling figures. """

import pygame
from pygame.locals import *

import game
import graphics
from config import Screen

class Block(pygame.sprite.Sprite):
    def __init__(self, img_name, color_key, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = graphics.load_image(img_name, color_key)
        self.move_into(pos)

    def move_into(self, new_pos):
        x, y = new_pos
        sz = Screen.PIXEL_BLOCK_SIZE
        self.rect = self.rect.move(x*sz, y*sz)

    def abs_move_into(self, new_pos):
        pixel_x, pixel_y = new_pos
        self.rect = self.rect.move(new_pos)

    def get_x(self):
        return self.rect.topleft[0] / Screen.PIXEL_BLOCK_SIZE

    def get_y(self):
        return self.rect.topleft[1] / Screen.PIXEL_BLOCK_SIZE

    def get_position(self):
        return self.get_x(), self.get_y()

    def move_block_right(self):
        self.rect = self.rect.move(Screen.PIXEL_BLOCK_SIZE, 0)

    def move_block_left(self):
        self.rect = self.rect.move((-1)*Screen.PIXEL_BLOCK_SIZE, 0)

    def move_block_down(self):
        self.rect = self.rect.move(0, Screen.PIXEL_BLOCK_SIZE)

    def move_block_up(self):
        self.rect = self.rect.move(0, (-1)*Screen.PIXEL_BLOCK_SIZE)


class BlockCreator:
    types = {
        'amazing_red_medium': 'redblock32.png',
        'amazing_yellow_medium': 'yellowblock32.png',
        'amazing_green_medium': 'greenblock32.png',
        'pixel_red_medium': 'pixelredblock32.png',
        'pixel_yellow_medium': 'pixelyellowblock32.png',
        'pixel_green_medium': 'pixelgreenblock32.png',
        'pixel_purple_medium': 'pixelpurpleblock32.png'
    }

    class IncorrectBlockType(Exception):
        pass

    @staticmethod
    def create_block(type: str, color_key, position):
        """ Creates block with selected type. Type should be choosen
            from BlockCreator.types dictionary.
        """
        if type not in BlockCreator.types.keys():
            raise BlockCreator.IncorrectBlockType
        image_name = BlockCreator.types[type]
        return Block(image_name, color_key, position)


class AbstractFigure(pygame.sprite.Group):
    def __init__(self, pos: tuple):
        pygame.sprite.Group.__init__(self)
        # position of the center of inner coordinate system in outer system
        # +----------------->
        # |................
        # |...##|##........
        # |...##|##........
        # |...--O-->.......
        # |...##|##........
        # |...##|##........
        # V.....V..........
        #
        # O - center of inner coordinate system
        self.left_dir = -1
        self.down_dir = 0
        self.right_dir = 1
        self.clockwise_dir = 2
        self.counterclockwise_dir = 3

        self.blocks = []
        self.block_type = None
        self.inner_center = pos
        self.inner_coordinates = []

        self.landed = False
        self.game_ref = None

    def _build(self):
        raise NotImplemented

    def _valid_position(self):
        fallen = self.game_ref.get_fallen_blocks()

        return all(map(Screen.BOARD_RECT.contains, self.blocks))\
            and not pygame.sprite.groupcollide(self, fallen, False, False)

    def _rotate_clockwise(self):
        from proto import Rotate
        self.inner_coordinates = Rotate.rotate_clockwise(self.inner_coordinates)

        for block in self.blocks:
            self.remove(block)
        self.blocks = []
        self._build()

    def _rotate_counterclockwise(self):
        from proto import Rotate
        self.inner_coordinates = Rotate.rotate_counterclockwise(self.inner_coordinates)

        for block in self.blocks:
            self.remove(block)
        self.blocks = []
        self._build()

    def _move_left(self):
        old = self.inner_center
        self.inner_center = old[0] - 1, old[1]
        for block in self.blocks:
            block.move_block_left()

    def _move_right(self):
        old = self.inner_center
        self.inner_center = old[0] + 1, old[1]
        for block in self.blocks:
            block.move_block_right()

    def _move_down(self):
        old = self.inner_center
        self.inner_center = old[0], old[1] + 1
        for block in self.blocks:
            block.move_block_down()

    def _move_helper(self, action: int):
        if action == self.left_dir:
            self._move_left()
            if not self._valid_position():
                self._move_right()

        elif action == self.right_dir:
            self._move_right()
            if not self._valid_position():
                self._move_left()

        elif action == self.clockwise_dir:
            self._rotate_clockwise()
            if not self._valid_position():
                self._rotate_counterclockwise()

        elif action == self.counterclockwise_dir:
            self._rotate_counterclockwise()
            if not self._valid_position():
                self._rotate_clockwise()

        elif action == self.down_dir:
            self._move_down()
            if not self._valid_position():
                self.landed = True
                old = self.inner_center
                self.inner_center = old[0], old[1] - 1
                for block in self.blocks:
                    block.move_block_up()

    def move_left(self):
        self._move_helper(self.left_dir)

    def move_right(self):
        self._move_helper(self.right_dir)

    def move_down(self):
        self._move_helper(self.down_dir)

    def rotate_clockwise(self):
        self._move_helper(self.clockwise_dir)

    def rotate_counterclockwise(self):
        self._move_helper(self.counterclockwise_dir)

    def is_landed(self):
        return self.landed

    def map_inner_to_outer(self, inner_coord):
        inner_center = complex(self.inner_center[0], self.inner_center[1])
        inner_coord = complex(inner_coord[0], inner_coord[1])
        result = inner_center + inner_coord
        return result.real, result.imag

    def set_game_ref(self, game_ref):
        self.game_ref = game_ref

    def get_center(self):
        return self.inner_center


class BaseFigure(AbstractFigure):
    def __init__(self, pos, block_type):
        AbstractFigure.__init__(self, pos)
        self.block_type = block_type
        self.game_ref = None
        self.pos = pos
        self.set_coordinates()
        self._build()

    def _build(self):
        outer_coords = map(self.map_inner_to_outer, self.inner_coordinates)
        for coord in outer_coords:
            block = BlockCreator.create_block(self.block_type, 255, coord)
            self.blocks.append(block)
            self.add(block)

    def set_coordinates(self):
        class AbstractObjectCreation(Exception):
            pass
        raise AbstractObjectCreation

    def copy_to(self, pos):
        obj = self.__class__(pos, self.block_type)
        return obj


class PlankFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-2, 0), (-1, 0), (0, 0), (1, 0)]


class SquareFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-1, -1), (0, -1), (-1, 0), (0, 0)]


class TFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-1, -1), (0, -1), (1, -1), (0, 0)]


class LFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-2, 0), (-1, 0), (0, -1), (0, 0)]


class ZFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-2, 0), (-1, -1), (-1, 0), (0, -1)]


class LMirrorFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-1, -1), (-1, 0), (0, 0), (1, 0)]


class ZMirrorFigure(BaseFigure):
    def set_coordinates(self):
        self.inner_coordinates = [(-1, -1), (0, -1), (0, 0), (1, 0)]