import enum

import numpy as np

import utils


class Direction(enum.Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


DIRECTIONS = {
    Direction.UP: np.array([0, 1]),
    Direction.DOWN: np.array([0, -1]),
    Direction.LEFT: np.array([-1, 0]),
    Direction.RIGHT: np.array([1, 0]),
}


def move(point, direction):
    return point + DIRECTIONS[direction]


def points(path):
    result = {}

    curr = np.array([0, 0])
    step = 0

    for edge in path:
        direction, length = Direction(edge[0]), int(edge[1:])

        for _ in range(length):
            step += 1
            curr = move(curr, direction)
            result[tuple(curr)] = step

    return result


def manhattan(point):
    return abs(point[0]) + abs(point[1])


def get_intersections(points_1, points_2):
    return set(points_1.keys()) & set(points_2.keys())


@utils.part
def part_1():
    path_1, path_2 = utils.get_input(cast=str)
    print(min(
        manhattan(intersection)
        for intersection in get_intersections(points(path_1), points(path_2))
    ))


@utils.part
def part_2():
    path_1, path_2 = utils.get_input(cast=str)
    points_1, points_2 = points(path_1), points(path_2)
    intersections = get_intersections(points_1, points_2)

    steps = [
        points_1[intersection] + points_2[intersection]
        for intersection in intersections
    ]

    print(min(steps))
