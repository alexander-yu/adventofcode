import math

import utils


class Grid(utils.Grid):
    def __getitem__(self, position):
        i, j = position
        return super().__getitem__((i, j % self.columns))


def get_trees_encountered(grid, slope):
    position = (0, 0)
    trees = 0

    while position[0] < grid.rows:
        trees += grid[position] == '#'
        position = utils.add_vector(position, slope)

    return trees


@utils.part
def part_1():
    grid = utils.get_grid(grid_cls=Grid, delimiter='', cast=str)
    print(get_trees_encountered(grid, (1, 3)))


@utils.part
def part_2():
    slopes = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ]
    grid = utils.get_grid(grid_cls=Grid, delimiter='', cast=str)
    print(math.prod(get_trees_encountered(grid, slope) for slope in slopes))
