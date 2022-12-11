import collections
import enum

from sly import Lexer

from utils import Vector

import utils


VECTORS = {
    'sw': Vector(-1, 0, -1),
    'se': Vector(0, -1, -1),
    'nw': Vector(0, 1, 1),
    'ne': Vector(1, 0, 1),
    'w': Vector(-1, 1, 0),
    'e': Vector(1, -1, 0),
}


class Color(enum.Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'

    @staticmethod
    def flip(color):
        if color == Color.WHITE:
            return Color.BLACK
        return Color.WHITE


class TileLexer(Lexer):
    # pylint: disable=used-before-assignment
    tokens = {SW, SE, NW, NE, W, E}
    SW = r'sw'
    SE = r'se'
    NW = r'nw'
    NE = r'ne'
    W = r'w'
    E = r'e'


def get_initial_floor():
    tiles = utils.get_input(delimiter=None, cast=str)
    lexer = TileLexer()
    floor = collections.defaultdict(lambda: Color.WHITE)

    for tile in tiles:
        position = (0, 0, 0)
        for token in lexer.tokenize(tile):
            position = position + VECTORS[token.value]

        floor[position] = Color.flip(floor[position])

    return floor


@utils.part
def part_1():
    floor = get_initial_floor()
    print(list(floor.values()).count(Color.BLACK))


@utils.part
def part_2():
    floor = get_initial_floor()

    for _ in range(100):
        black_neighbors = collections.defaultdict(int)

        for position, color in floor.items():
            if color == Color.BLACK:
                neighbor_colors = []

                for vector in VECTORS.values():
                    neighbor = position + vector
                    neighbor_colors.append(floor.get(neighbor, Color.WHITE))
                    black_neighbors[neighbor] += 1

                if all([color == Color.WHITE for color in neighbor_colors]):
                    black_neighbors[position] = 0

        for position, count in black_neighbors.items():
            color = floor[position]
            if color == Color.BLACK and count not in [1, 2]:
                floor[position] = Color.flip(color)
            elif color == Color.WHITE and count == 2:
                floor[position] = Color.flip(color)

    print(list(floor.values()).count(Color.BLACK))
