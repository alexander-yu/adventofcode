import numpy as np

import utils


def get_data():
    return np.array(utils.get_input(delimiter=''))


def is_visible(grid, i, j):
    height = grid[i, j]

    max_l = max(grid[i, :j], default=-1)
    max_r = max(grid[i, j + 1:], default=-1)
    max_u = max(grid[:i, j], default=-1)
    max_d = max(grid[i + 1:, j], default=-1)

    return any(h < height for h in [max_l, max_r, max_u, max_d])


def visibility_score(grid, i, j):
    rows, columns = grid.shape
    height = grid[i, j]
    score = 1

    for direction in utils.DIRECTIONS.values():
        distance = 0
        current = (i, j) + direction

        while 0 <= current[0] < rows and 0 <= current[1] < columns:
            distance += 1

            if grid[current] >= height:
                break

            current += direction

        score *= distance

    return score


@utils.part
def part_1():
    grid = get_data()
    rows, columns = grid.shape

    print(sum(is_visible(grid, i, j) for i in range(rows) for j in range(columns)))


@utils.part
def part_2():
    grid = get_data()
    rows, columns = grid.shape

    print(max(visibility_score(grid, i, j) for i in range(rows) for j in range(columns)))
