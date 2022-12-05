import collections
import enum
import itertools

import numpy as np

import utils


VECTORS = [
    np.array([0, 1, 0]),
    np.array([0, -1, 0]),
    np.array([1, 0, 0]),
    np.array([-1, 0, 0]),
]

CENTER = (2, 2)


class Tile(enum.Enum):
    BUG = '#'
    EMPTY = '.'


class Grid:
    def __init__(self, grid=None, recursive=True):
        level = new_layer()

        if grid:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    level[(i, j)] = grid[i][j]

        self.levels = {0: level}
        self.recursive = recursive

    def get(self, coordinate):
        i, j, k = coordinate
        if k not in self.levels:
            return Tile.EMPTY.value

        return self.levels[k][(i, j)]

    def set(self, coordinate, val):
        i, j, k = coordinate
        if k not in self.levels:
            self.levels[k] = new_layer()

        self.levels[k][(i, j)] = val

    def values(self, k):
        sorted_items = sorted(self.levels[k].items(), key=lambda item: item[0])
        return [value for _, value in sorted_items]

    def neighbors(self, coordinate):
        neighbors = []
        for vector in VECTORS:
            neighbor = utils.add_vector(coordinate, vector)
            val = self.get(neighbor)
            if val is not None:
                neighbors.append(val)

        if not self.recursive:
            return neighbors

        i, j, k = coordinate
        more_neighbors = []
        if (i, j) == (2, 1):
            more_neighbors = itertools.product(range(5), [0], [k + 1])
        elif (i, j) == (2, 3):
            more_neighbors = itertools.product(range(5), [4], [k + 1])
        elif (i, j) == (1, 2):
            more_neighbors = itertools.product([0], range(5), [k + 1])
        elif (i, j) == (3, 2):
            more_neighbors = itertools.product([4], range(5), [k + 1])
        else:
            if i == 0:
                more_neighbors.append((1, 2, k - 1))
            elif i == 4:
                more_neighbors.append((3, 2, k - 1))

            if j == 0:
                more_neighbors.append((2, 1, k - 1))
            elif j == 4:
                more_neighbors.append((2, 3, k - 1))

        for neighbor in more_neighbors:
            val = self.get(neighbor)
            if val is not None:
                neighbors.append(val)

        return neighbors

    def get_next(self, coordinate):
        val = self.get(coordinate)
        neighbors = self.neighbors(coordinate)
        bugs = [neighbor for neighbor in neighbors if neighbor == Tile.BUG.value]

        if val == Tile.BUG.value:
            if len(bugs) != 1:
                return Tile.EMPTY.value
        else:
            if len(bugs) in [1, 2]:
                return Tile.BUG.value

        return val

    def hash(self, k):
        return hash(''.join(self.values(k)))


def new_layer():
    return collections.defaultdict(lambda: Tile.EMPTY.value)


def biodiversity(grid, k):
    bugs = [tile == Tile.BUG.value for tile in grid.values(k)]
    return sum((1 << i) * is_bug for i, is_bug in enumerate(bugs))


def bugs(grid):
    n = 0
    for level in grid.levels:
        n += sum(tile == Tile.BUG.value for tile in grid.values(level))

    return n


@utils.part
def part_1():
    grid = Grid(utils.get_input(__file__, delimiter='', cast=str), recursive=False)
    hashes = set([grid.hash(0)])

    while True:
        new_grid = Grid(recursive=False)
        for coordinate in itertools.product(range(5), range(5), range(1)):
            new_grid.set(coordinate, grid.get_next(coordinate))

        new_hash = new_grid.hash(0)
        if new_hash in hashes:
            print(biodiversity(new_grid, 0))
            break

        hashes.add(new_hash)
        grid = new_grid


@utils.part
def part_2():
    grid = Grid(utils.get_input(__file__, delimiter='', cast=str))

    for i in range(200):
        new_grid = Grid(recursive=True)
        min_level = min(grid.levels.keys())
        max_level = max(grid.levels.keys())

        for coordinate in itertools.product(range(5), range(5), range(min_level - 1, max_level + 2)):
            if coordinate[:2] == CENTER:
                continue
            new_grid.set(coordinate, grid.get_next(coordinate))

        grid = new_grid
    print(bugs(grid))
