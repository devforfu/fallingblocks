import unittest

from grid import *


class GridTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = Grid()

    def tearDown(self):
        pass

    def test_str(self):
        assert self.obj.__str__() == "...\n...\n...\n", "__str__() failed"

    def test_toList(self):
        assert self.obj.toList() == ['.' for i in range(9)], "toList() failed"

    def test_getitem(self):
        assert self.obj[1][1] == '.', "__getitem__(), case 1: failed"
        try:
            self.obj[10][1]
        except InvalidIndex as e:
            assert e.message == "Grid index 10 is out of grid range", "__getitem__() case 2: failed"

    def test_copy(self):
        from functools import reduce
        self.obj[1][1] = 'x'
        another = self.obj.copy()
        another[0][0] = 'o'
        another[2][2] = 'o'
        assert not self.obj == another, "copy and original are equal"
        assert ''.join(reduce(lambda a, b: a+b, another.toList())) == 'o...x...o', "incorrect coping"

    def test_setitem(self):
        self.obj[2] = ['x','x','x']
        assert self.obj[2] == ['x','x','x'], "Incorrect row assignment"

    def test_setpattern(self):
        self.obj.setpattern(1, 'oxo')
        assert self.obj[1] == [c for c in 'oxo'], "Incorrect string pattern assignment"

    def test_in(self):
        pass

class CoordGridTestCase(unittest.TestCase):
    def setUp(self):
        self.m = CoordGrid(4, 4)

    def test_indexation(self):
        assert not self.m(2, 2), "Indexation error"
        self.m.set(2, 2)
        assert self.m(2, 2), "Assigment error"

        for index in range(4):
            self.m.set(index, index)

        for index in range(4):
            self.m.clear(index, index)

    def test_setclear_all(self):
        pass
        # self.m.set_all()
        # assert all(self.m.toList()), "set_all() function error"
        # self.m.clear_all()
        # assert not any(self.m.toList()), "clear_all() function error"


class BoardCoordsCase(unittest.TestCase):
    def setUp(self):
        self.m = BoardCoords(5, 6)

    def test_shift(self):
        w, h = self.m.width, self.m.height
        for col in range(w):
            self.m.set(h-1, col)
        self.m.set(h-2, 0)
        self.m.set(h-2, 3)
        self.m.set(h-2, 4)
        self.m.set(h-3, 3)
        print(self.m)
        self.m.shift(2)
        print(self.m)

if __name__ == "__main__":
    unittest.main()