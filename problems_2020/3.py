import math

from utils import Vector

import utils


class Grid(utils.Grid):
    def __getitem__(self, position):
        i, j = position
        return super().__getitem__((i, j % self.columns))


def get_trees_encountered(grid, slope):
    position = Vector(0, 0)
    trees = 0

    while position[0] < grid.rows:
        trees += grid[position] == '#'
        position += slope

    return trees


@utils.part
def part_1():
    grid = utils.get_grid(grid_cls=Grid, delimiter='', cast=str)
    print(get_trees_encountered(grid, (1, 3)))


@utils.part
def part_2():
    slopes = [
        Vector(1, 1),
        Vector(1, 3),
        Vector(1, 5),
        Vector(1, 7),
        Vector(2, 1),
    ]
    grid = utils.get_grid(grid_cls=Grid, delimiter='', cast=str)
    print(math.prod(get_trees_encountered(grid, slope) for slope in slopes))
