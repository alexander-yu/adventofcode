import enum
import os
import pathlib
import re

import numpy as np


ORIGIN = np.array([
    [0],
    [0],
])


class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


DIRECTIONS = {
    Direction.NORTH: np.array([
        [0],
        [1],
    ]),
    Direction.EAST: np.array([
        [1],
        [0],
    ]),
    Direction.SOUTH: np.array([
        [0],
        [-1],
    ]),
    Direction.WEST: np.array([
        [-1],
        [0],
    ]),
}

ROTATIONS = [
    np.array(
        [[1, 0],
         [0, 1]]
    ),
    np.array(
        [[0, -1],
         [1, 0]]
    ),
    np.array(
        [[-1, 0],
         [0, -1]]
    ),
    np.array(
        [[0, 1],
         [-1, 0]]
    ),
]


def _split_line(line, delimiter, cast):
    if delimiter == '':
        return list(cast(ch) for ch in line)
    if delimiter is None:
        return cast(line)

    if isinstance(delimiter, list):
        items = re.split('|'.join(delimiter), line)
    else:
        assert isinstance(delimiter, str)
        items = line.split(delimiter)

    return [cast(item) for item in items]


# pylint: disable=too-many-arguments
def get_input(problem_file, test=False, delimiter=',', cast=int, line_delimiter='\n', rstrip=None):
    problem_path = pathlib.Path(problem_file).resolve()
    problem_number = problem_path.stem
    test_prefix = '_test' if test else ''
    input_file_name = f'{problem_number}{test_prefix}.txt'

    with open(os.path.join(problem_path.parent, 'inputs', input_file_name), 'r') as f:
        lines = f.read().rstrip().split(line_delimiter)

    if rstrip:
        lines = [line.rstrip(rstrip) for line in lines]

    return [
        _split_line(line, delimiter, cast)
        for line in lines
    ]


def to_vector(tup):
    return np.reshape(np.array(tup), (-1, 1))


def add_vector(position, vector):
    return tuple(x + y for x, y in zip(position, vector))


class MultiValueEnum(enum.Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    def values(self):
        cls = type(self)
        return [value for value in cls._value2member_map_ if cls._value2member_map_[value] == self]
