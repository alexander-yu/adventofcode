import math

import click

import utils


class Grid:
    def __init__(self):
        self.points = utils.get_input(__file__, delimiter='', cast=str)
        self.rows = len(self.points)
        self.columns = len(self.points[0])

    def __getitem__(self, position):
        i, j = position
        return self.points[i][j % self.columns]


def get_trees_encountered(grid, slope):
    position = (0, 0)
    trees = 0

    while position[0] < grid.rows:
        trees += grid[position] == '#'
        position = utils.add_vector(position, slope)

    return trees


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    grid = Grid()
    print(get_trees_encountered(grid, (1, 3)))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    slopes = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ]
    grid = Grid()
    print(math.prod(get_trees_encountered(grid, slope) for slope in slopes))


if __name__ == '__main__':
    cli()
