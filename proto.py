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