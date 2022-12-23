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


def get_password(point, direction):
    x, y = point

    row = -y + 1
    col = x + 1

    facing = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1): 3,
    }[direction]

    return 1000 * row + col + facing


@utils.part
def part_1():
    start, grid, path, points_by_x, points_by_y = get_data()
    direction = Vector2D(1, 0)

    curr = start

    for move in path:
        match move:
            case 'L': direction = direction.rot90(1)
            case 'R': direction = direction.rot90(3)
            case _:
                for _ in range(move):
                    new = curr + direction

                    if new not in grid:
                        match direction.sign():
                            case 1, _: new = points_by_y[new[1]][0]
                            case -1, _: new = points_by_y[new[1]][-1]
                            case _, 1: new = points_by_x[new[0]][-1]
                            case _, -1: new = points_by_x[new[0]][0]

                    if grid[new] == '#':
                        break

                    curr = new

    print(get_password(curr, direction))


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
    (1, -1, 0): lambda x, y, points_by_x, points_by_y: (points_by_y[-150 + y + 1][0], Vector2D(1, 0)),
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

    return WRAPS[face, *direction.sign()](x, y, points_by_x, points_by_y)


@utils.part
def part_2():
    start, grid, path, points_by_x, points_by_y = get_data()
    direction = Vector2D(1, 0)

    curr = start

    for move in path:
        match move:
            case 'L': direction = direction.rot90(1)
            case 'R': direction = direction.rot90(3)
            case _:
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

    print(get_password(curr, direction))
