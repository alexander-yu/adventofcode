import collections
import re

from utils import Vector2D

import utils


def get_data():
    *points, _, path = utils.get_input(cast=str, delimiter=None)
    start, grid, points_by_x, points_by_y = get_grid(points)
    path = [
        int(move) if move.isnumeric() else move
        for move in re.findall(r'\d+|L|R', path)
    ]

    return start, grid, path, points_by_x, points_by_y


def get_grid(point_rows):
    points = {}
    n_rows = 0
    n_columns = 0
    start = None
    points_by_x = collections.defaultdict(list)
    points_by_y = collections.defaultdict(list)

    for i, row in enumerate(point_rows):
        n_rows = i + 1
        for j, value in enumerate(row):
            n_columns = j + 1

            if value != ' ':
                point = Vector2D(j, -i)
                points_by_x[j].append(point)
                points_by_y[-i].append(point)
                points[point] = value
                if not start:
                    start = point

    return start, utils.Grid(points, n_rows, n_columns), points_by_x, points_by_y


@utils.part
def part_1():
    start, grid, path, points_by_x, points_by_y = get_data()
    direction = Vector2D(1, 0)

    curr = start

    for move in path:
        if isinstance(move, int):
            for _ in range(move):
                new = curr + direction
                if new not in grid:
                    if direction[0] > 0:
                        new = points_by_y[new[1]][0]
                    elif direction[0] < 0:
                        new = points_by_y[new[1]][-1]
                    elif direction[1] > 0:
                        new = points_by_x[new[0]][-1]
                    elif direction[1] < 0:
                        new = points_by_x[new[0]][0]
                    else:
                        raise ValueError(direction)

                if grid[new] == '#':
                    break

                curr = new
        elif move == 'L':
            direction = direction.rot90(1)
        else:
            direction = direction.rot90(3)

    x, y = curr
    row = -y + 1
    col = x + 1
    facing = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1): 3,
    }[direction]

    print(1000 * row + 4 * col + facing)


FACES = {
    (1, 0): 1,
    (2, 0): 2,
    (1, 1): 3,
    (0, 2): 4,
    (1, 2): 5,
    (0, 3): 6,
}


def get_face(point):
    x, y = point
    x, y = x // 50, -y // 50
    return FACES[x, y]


WRAPS = {
    (1, 0, 1): lambda x, y, points_by_x, points_by_y: (points_by_y[-150 - x][0], Vector2D(1, 0)),
    (1, -1,  0): lambda x, y, points_by_x, points_by_y: (points_by_y[-150 + y + 1][0], Vector2D(1, 0)),
    (2, 0, 1): lambda x, y, points_by_x, points_by_y: (points_by_x[x][-1], Vector2D(0, 1)),
    (2, 1, 0): lambda x, y, points_by_x, points_by_y: (points_by_y[-150 + y][-1], Vector2D(-1, 0)),
    (2, 0, -1): lambda x, y, points_by_x, points_by_y: (points_by_y[-50 - x][-1], Vector2D(-1, 0)),
    (3, -1, 0): lambda x, y, points_by_x, points_by_y: (points_by_x[y][0], Vector2D(0, -1)),
    (3, 1, 0): lambda x, y, points_by_x, points_by_y: (points_by_x[100 + y][-1], Vector2D(0, 1)),
    (4, -1, 0): lambda x, y, points_by_x, points_by_y: (points_by_y[-50 + y + 1][0], Vector2D(1, 0)),
    (4, 0, 1): lambda x, y, points_by_x, points_by_y: (points_by_y[-50 - x][0], Vector2D(1, 0)),
    (5, 1, 0): lambda x, y, points_by_x, points_by_y: (points_by_y[-50 + y][-1], Vector2D(-1, 0)),
    (5, 0, -1): lambda x, y, points_by_x, points_by_y: (points_by_y[-150 - x][-1], Vector2D(-1, 0)),
    (6, -1, 0): lambda x, y, points_by_x, points_by_y: (points_by_x[50 + y][0], Vector2D(0, -1)),
    (6, 1, 0): lambda x, y, points_by_x, points_by_y: (points_by_x[50 + y][-1], Vector2D(0, 1)),
    (6, 0, -1): lambda x, y, points_by_x, points_by_y: (points_by_x[100 + x][0], Vector2D(0, -1)),
}


def wrap(point, direction, points_by_x, points_by_y):
    face = get_face(point)

    x, y = point
    x, y = x % 50, 50 - (y % 50)

    return WRAPS[face, utils.sign(direction[0]), utils.sign(direction[1])](x, y, points_by_x, points_by_y)


@utils.part
def part_2():
    start, grid, path, points_by_x, points_by_y = get_data()
    direction = Vector2D(1, 0)

    curr = start

    for move in path:
        if isinstance(move, int):
            for _ in range(move):
                new = curr + direction
                if new not in grid:
                    new, new_direction = wrap(curr, direction, points_by_x, points_by_y)
                else:
                    new_direction = direction

                if grid[new] == '#':
                    break

                curr = new
                direction = new_direction
        elif move == 'L':
            direction = direction.rot90(1)
        else:
            direction = direction.rot90(3)

    x, y = curr
    row = -y + 1
    col = x + 1
    facing = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1): 3,
    }[direction]

    print(1000 * row + 4 * col + facing)
