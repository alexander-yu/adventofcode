import collections
import copy
import enum
import functools
import itertools
import os
import pathlib
import re
import typing

import numpy as np


PART_REGISTRY = collections.defaultdict(dict)
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


def _split_line(
    line: str,
    delimiter: typing.Union[str, None],
    cast: typing.Callable[[str], typing.Any],
):
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
def get_input(
    problem_file: str,
    test: bool = False,
    delimiter: typing.Union[str, None] = ',',
    cast: typing.Callable[[str], typing.Any] = int,
    line_delimiter: str = '\n',
    rstrip: typing.Union[str, None] = None,
):
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


def add_vector(position: tuple, vector: tuple):
    return tuple(x + y for x, y in zip(position, vector))


def get_neighbors(point: tuple):
    dims = len(point)
    zero = tuple(0 for _ in range(dims))

    for vector in itertools.product([-1, 0, 1], repeat=dims):
        if vector != zero:
            yield add_vector(point, vector)


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


class Grid:
    def __init__(
        self,
        points: typing.Dict[typing.Tuple[int, int], typing.Any],
        rows: int,
        columns: int,
    ):
        self.points = points
        self.rows = rows
        self.columns = columns

    def __getitem__(self, point: typing.Tuple[int, int]):
        return self.points[point]

    def __setitem__(self, point: typing.Tuple[int, int], value):
        self.points[point] = value

    def clone(self):
        return type(self)(copy.deepcopy(self.points), self.rows, self.columns)


def get_grid(
    problem_file: str,
    grid_cls: typing.Type[Grid] = Grid,
    value_transformer: typing.Callable[[typing.Any], typing.Any] = lambda x: x,
    **get_input_kwargs
):
    points = {}
    rows = 0
    columns = 0

    for i, row in enumerate(get_input(problem_file, **get_input_kwargs)):
        rows = i + 1
        for j, value in enumerate(row):
            columns = j + 1
            points[(i, j)] = value_transformer(value)

    return grid_cls(points, rows, columns)


def part(path: str, part_number: int):
    def wrapper(wrapped):
        PART_REGISTRY[path][part_number] = wrapped

        @functools.wraps(wrapped)
        def inner(*args, **kwargs):
            return wrapped(*args, **kwargs)

        return inner
    return wrapper
