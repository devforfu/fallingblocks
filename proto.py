""" Prototyping of figure rotation """


class Rotate:
    mapper1 = {
        (-1, 0): (0, 0),
        (0, 0): (0, -1),
        (0, -1): (-1, -1),
        (-1, -1): (-1, 0)
    }
    mapper2 = {
        (-2, 0): (0, 1),
        (0, 1): (1, -1),
        (1, -1): (-1, -2),
        (-1, -2): (-2, 0),
        (1, 0): (0, -2),
        (0, -2): (-2, -1),
        (-2, -1): (-1, 1),
        (-1, 1): (1, 0)
    }

    @staticmethod
    def console(fig):
        matrix = []
        for x in [-2, -1, 0, 1]:
            for y in [-2, -1, 0, 1]:
                if (y, x) in fig:
                    matrix.append('#')
                else:
                    matrix.append('.')
            matrix.append('\n')
        print(''.join(matrix))


    @staticmethod
    def rotate_counterclockwise(fig):
        def transform(coord):
            return Rotate.mapper1[coord] if coord in Rotate.mapper1 else Rotate.mapper2[coord]
        return list(map(transform, fig))

    @staticmethod
    def rotate_clockwise(fig):
        def transform(coord):
            mapper1 = {v: k for k, v in Rotate.mapper1.items()}
            mapper2 = {v: k for k, v in Rotate.mapper2.items()}
            return mapper1[coord] if coord in mapper1 else mapper2[coord]
        return list(map(transform, fig))


class ConnectedComponents:
    """ Takes list of coordinates and returns list of lists
        with connected points

        >>> cc = ConnectedComponents.search([(5,2), (6,2), (8,6), (8,8), (8,9), (9,8), (9, 9)])
        >>> for line in cc: print(cc)
        [(5, 2), (6, 2)]
        [(8, 6)]
        [(8, 8), (8, 9), (9, 8), (9, 9)]
    """
    @staticmethod
    def left(pos):
        x, y = pos
        if x < 1:
            return None
        return x-1, y

    @staticmethod
    def right(pos):
        x, y = pos
        if x >= 10:
            return None
        return x+1, y

    @staticmethod
    def up(pos):
        x, y = pos
        if y < 1:
            return None
        return x, y-1

    @staticmethod
    def down(pos):
        x, y = pos
        if y >= 10:
            return None
        return x, y+1

    @staticmethod
    def search(coords):
        import collections
        cc = ConnectedComponents
        connected_components = []
        while coords:
            start, coords = coords[0], coords[1:]
            closed = [start]
            fringe = collections.deque()
            fringe.append(start)

            while fringe:
                u = fringe.popleft()
                neighbors = cc.left(u), cc.right(u), cc.up(u), cc.down(u)
                for pair in neighbors:
                    if pair not in coords:
                        continue
                    if pair is not None and pair not in closed:
                        fringe.append(pair)
                        closed.append(pair)
                        coords.remove(pair)

            connected_components.append(closed)

        return connected_components


if __name__ == '__main__':
    plank = [(-2, 0), (-1, 0), (0, 0), (1, 0)]
    theta = [(-1, -1), (0, -1), (0, 0), (1, -1)]
    square = [(-1, -1), (-1, 0), (0, -1), (0, 0)]
    el = [(-2, 0), (-1, 0), (0, 0), (0, -1)]
    zet = [(-2, 0), (-1, 0), (-1, -1), (0, -1)]

    figures = [plank, theta, square, el, zet]
    names = ['plank', 'T-letter', 'square', 'L-letter', 'Z-letter']
    i = 0
    for figure in figures:
        print('name: ', names[i])
        print('-- clockwise --')
        for _ in range(5):
            Rotate.console(figure)
            figure = Rotate.rotate_clockwise(figure)
        print('-- counterclockwise -- ')
        for _ in range(5):
            Rotate.console(figure)
            figure = Rotate.rotate_counterclockwise(figure)
        print('-'*40)
        i += 1