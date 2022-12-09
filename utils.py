from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import collections
import copy
import dataclasses
import enum
import inspect
import itertools
import os
import pathlib
import re

from boltons import iterutils

import networkx as nx
import numpy as np
import parse as parselib


PART_REGISTRY = collections.defaultdict(dict)
IS_TEST = False


class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Vector(tuple):
    def __new__(cls, *args):
        if len(args) > 1:
            return super().__new__(cls, args)
        return super().__new__(cls, args[0])

    def __add__(self, other):
        return self.__class__(x + y for x, y in zip(self, other))

    def __radd__(self, other):
        return self.__class__(x + y for x, y in zip(other, self))

    def __sub__(self, other):
        return self.__class__(x - y for x, y in zip(self, other))

    def __rsub__(self, other):
        return self.__class__(x - y for x, y in zip(other, self))

    def __mul__(self, other):
        return self.__class__(x * other for x in self)

    def __rmul__(self, other):
        return self.__class__(other * x for x in self)

    def abs(self):
        return self.__class__(abs(x) for x in self)

    def sign(self):
        return self.__class__(sign(x) for x in self)

    def dist(self, metric='manhattan'):
        if metric == 'manhattan':
            return sum(self.abs())

        raise ValueError(f'Unsupported distance metric {metric}')


class Vector2D(Vector):
    DIRECTION_ALIASES = {
        **dict.fromkeys([Direction.NORTH, 'N', 'U', 'n', 'u', 'north', 'NORTH', 'up',  'UP'], Direction.NORTH),
        **dict.fromkeys([Direction.EAST, 'E', 'R', 'e', 'r', 'east', 'EAST', 'right',  'RIGHT'], Direction.EAST),
        **dict.fromkeys([Direction.SOUTH, 'S', 'D', 's', 'd', 'south', 'SOUTH', 'down',  'DOWN'], Direction.SOUTH),
        **dict.fromkeys([Direction.WEST, 'W', 'L', 'w', 'l', 'west', 'WEST', 'left',  'LEFT'], Direction.WEST),
    }

    def __new__(cls, *args):
        vector = super().__new__(cls, *args)
        assert len(vector) == 2
        return vector

    def rot90(self, k: int = 1):
        k %= 4
        x, y = self

        if k == 1:
            return Vector2D(-y, x)
        if k == 2:
            return Vector2D(-x, -y)
        if k == 3:
            return Vector2D(y, -x)

        return self

    def shift(self, direction: str) -> Vector2D:
        return self + DIRECTIONS[self.DIRECTION_ALIASES[direction]]


NP_ORIGIN = np.array([
    [0],
    [0],
])

NP_DIRECTIONS = {
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

ORIGIN = Vector2D(0, 0)

DIRECTIONS = {
    Direction.NORTH: Vector2D(0, 1),
    Direction.EAST: Vector2D(1, 0),
    Direction.SOUTH: Vector2D(0, -1),
    Direction.WEST: Vector2D(-1, 0),
}


ROTATIONS_2D = [
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


ROTATIONS_3D = [
    permutation * signs
    for permutation, signs in itertools.product(
        [
            np.array(permutation)
            for permutation in itertools.permutations(np.identity(3, dtype=int))
        ],
        [
            np.array(signs)
            for signs in itertools.product([-1, 1], repeat=3)
        ],
    )
    if np.linalg.det(permutation * signs) == 1
]


def _split_line(
    line: str,
    delimiter: Optional[str],
    cast: Callable[[str], Any],
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
def parse(
    content: str,
    delimiter: Optional[str] = ',',
    cast: Callable[[str], Any] = int,
    line_delimiter: str = '\n',
    rstrip: str = '',
    remove_suffix: str = '',
    remove_prefix: str = '',
    format: Optional[str] = None,
):
    lines = content.rstrip().split(line_delimiter)
    lines = [
        line
        .rstrip(rstrip)
        .removeprefix(remove_prefix)
        .removesuffix(remove_suffix)
        for line in lines
    ]

    if format:
        return [parselib.parse(format, line) for line in lines]

    return [
        _split_line(line, delimiter, cast)
        for line in lines
    ]


# pylint: disable=too-many-arguments
def get_input(
    problem_file: str,
    delimiter: Optional[str] = ',',
    cast: Callable[[str], Any] = int,
    line_delimiter: str = '\n',
    rstrip: Optional[str] = None,
    remove_suffix: str = '',
    remove_prefix: str = '',
    format: Optional[str] = None,
):
    problem_path = pathlib.Path(problem_file).resolve()
    problem_number = problem_path.stem
    test_prefix = '_test' if IS_TEST else ''
    input_file_name = f'{problem_number}{test_prefix}.txt'

    with open(os.path.join(problem_path.parent, 'inputs', input_file_name), 'r') as f:
        return parse(
            f.read(),
            delimiter=delimiter,
            cast=cast,
            line_delimiter=line_delimiter,
            rstrip=rstrip,
            remove_suffix=remove_suffix,
            remove_prefix=remove_prefix,
            format=format,
        )


def add_vector(position: tuple, vector: tuple):
    return tuple(x + y for x, y in zip(position, vector))


def subtract_vector(position: tuple, vector: tuple):
    return tuple(x - y for x, y in zip(position, vector))


def sign(x: Union[float, int]) -> int:
    if x > 0:
        return 1

    if x < 0:
        return -1

    return 0


def get_neighbors(point: tuple, include_diagonals: bool = False):
    dims = len(point)
    zero = tuple(0 for _ in range(dims))

    for vector in itertools.product([-1, 0, 1], repeat=dims):
        if vector != zero and (include_diagonals or sum(vector) == 1):
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
        points: Dict[Tuple[int, int], Any],
        rows: int,
        columns: int,
    ):
        self.points = points
        self.rows = rows
        self.columns = columns
        self.graph = self.to_graph()

    def __getitem__(self, point: Tuple[int, int]):
        return self.points[point]

    def __setitem__(self, point: Tuple[int, int], value):
        self.points[point] = value

    def __iter__(self):
        for point in self.points:
            yield point

    def __len__(self):
        return len(self.points)

    def items(self):
        for point, value in self.points.items():
            yield point, value

    def neighbors(self, point: Tuple[int, int]):
        for neighbor in self.graph.neighbors(point):
            yield neighbor

    def clone(self):
        return type(self)(copy.deepcopy(self.points), self.rows, self.columns)

    def to_graph(self):
        graph = nx.Graph()
        for point, value in self.points.items():
            graph.add_node(point, value=value)

        for point in self.points:
            for neighbor in get_neighbors(point):
                if neighbor in self.points:
                    graph.add_edge(point, neighbor)

        return graph


class DiagonalGrid(Grid):
    def to_graph(self):
        graph = nx.Graph()
        for point, value in self.points.items():
            graph.add_node(point, value=value)

        for point in self.points:
            for neighbor in get_neighbors(point, include_diagonals=True):
                if neighbor in self.points:
                    graph.add_edge(point, neighbor)

        return graph


class DirectedGrid(Grid):
    def to_graph(self):
        graph = nx.DiGraph()
        for point, value in self.points.items():
            graph.add_node(point, value=value)

        for point in self.points:
            for neighbor in get_neighbors(point):
                if neighbor in self.points:
                    graph.add_edge(point, neighbor)
                    graph.add_edge(neighbor, point)

        return graph


def get_grid(
    problem_file: str,
    input_transformer: Callable[[Any], Any] = lambda x: x,
    grid_cls: Type[Grid] = Grid,
    value_transformer: Callable[[Any], Any] = lambda x: x,
    **get_input_kwargs
):
    points = {}
    rows = 0
    columns = 0

    for i, row in enumerate(input_transformer(get_input(problem_file, **get_input_kwargs))):
        rows = i + 1
        for j, value in enumerate(row):
            columns = j + 1
            points[(i, j)] = value_transformer(value)

    return grid_cls(points, rows, columns)


def assert_one(iterable, key=None):
    item = iterutils.one(iterable, key=key)
    assert item is not None
    return item


@dataclasses.dataclass(frozen=True)
class Part:
    id: str
    cmd: Callable


def part(func):
    calling_frame = inspect.currentframe().f_back
    calling_module = inspect.getmodule(calling_frame)
    path = calling_module.__name__
    part_id = func.__name__.removeprefix('part_')

    PART_REGISTRY[path][str(part_id)] = Part(part_id, func)
    return func
