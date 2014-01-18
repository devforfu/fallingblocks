from exceptions import *

# FIXME: Incorrent 'in' operation working


class Grid:
    def __init__(self, defaultfill='.', width=3, height=3):
        self.fillchar = defaultfill
        self.width = width
        self.height = height
        self.size = (width, height)
        self._grid = [[defaultfill for _ in range(width)] for _ in range(height)]

    def __getitem__(self, item):
        if item >= self.height:
            raise InvalidIndex('Grid index {0} is out of grid range'.format(item))
        return self._grid[item]

    def __setitem__(self, key, item):
        self._grid[key] = item

    def __str__(self):
        s = []
        for row in self._grid:
            for char in row:
                s.append(char)
            s.append('\n')
        return ''.join(s)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Grid):
            raise TypeError('Grid object cannot be compared with ' + other.__name__)
        return self._grid == other._grid

    def copy(self):
        g = Grid(self.fillchar, self.width, self.height)
        g._grid = [x[:] for x in self._grid]
        return g

    def toList(self):
        acc = []
        for row in self._grid:
            acc += row
        return acc

    def setpattern(self, index, pattern:str):
        """ pattern is a string looks like 'abcd' """
        self.__setitem__(index, [c for c in pattern])


class CoordGrid(Grid):
    """ Used for representation of inner coordinate system
        of falling figures. This grid has 4 x 4 size
        and special indexation (see examples below).

        >>> g = CoordGrid()
    """
    def __init__(self, w: int, h: int):
        Grid.__init__(self, defaultfill=False, width=w, height=h)

    def __getitem__(self, item):
        raise NotImplemented

    def __setitem__(self, key, value):
        raise NotImplemented

    def __str__(self):
        s = []
        for row in self._grid:
            for val in row:
                s.append('#' if val else '.')
            s.append('\n')
        return ''.join(s)

    def __call__(self, row: int, col: int):
        if row >= self.height:
            raise InvalidIndex('Row index {0} is out of grid range'
                                .format(row))
        if col >= self.width:
            raise InvalidIndex('Column index {0} is out of grid range'
                                .format(col))
        return self._grid[row][col]

    def setpattern(self, index, pattern: list):
        """ Overriden method from Grid class. Treat pattern
            as list of boolean values
        """
        self.__setitem__(index, [bool(c) for c in pattern])

    def set(self, row, col):
        self._grid[row][col] = True

    def clear(self, row, col):
        self._grid[row][col] = False


class InnerCoords(CoordGrid):
    def __init__(self):
        CoordGrid.__init__(self, 4, 4)


class BoardCoords(CoordGrid):
    def __init__(self, w: int, h: int):
        CoordGrid.__init__(self, w, h)

    def clear_all(self):
        for row in range(self.height):
            self._grid[row] = [False] * self.width

    def shift(self, count):
        while count:
            for row in range(self.height-2, 1, -1):
                self._grid[row+1] = self._grid[row]
            self._grid[0] = [False] * self.width
            count -= 1
