import dataclasses
import itertools

from utils import Vector2D

import utils


BLIZZARD_DIRECTIONS = {
    '<': 'L',
    '>': 'R',
    '^': 'U',
    'v': 'D',
}


@dataclasses.dataclass
class Blizzard:
    position: Vector2D
    direction: str

    def move(self, valley):
        position = self.position.shift(self.direction)

        if position not in valley.points:
            x, y = position

            x = (x - 1) % valley.cols + 1
            y = (y - 1) % valley.rows + 1

            position = Vector2D(x, y)

        return Blizzard(position, self.direction)


@dataclasses.dataclass
class Valley:
    entrance: Vector2D
    exit: Vector2D
    points: set
    blizzards: list
    blizzard_points: set
    rows: int
    cols: int

    @staticmethod
    def from_input(rows):
        entrance_point = Vector2D(rows[0].index('.'), len(rows) - 1)
        exit_point = Vector2D(rows[-1].index('.'),  0)
        points = set()
        blizzards = []

        for i, row in enumerate(rows[::-1]):
            for j, value in enumerate(row):
                if value != '#':
                    point = Vector2D(j, i)
                    points.add(point)

                    if value in BLIZZARD_DIRECTIONS:
                        blizzards.append(Blizzard(point, BLIZZARD_DIRECTIONS[value]))

        return Valley(
            entrance=entrance_point,
            exit=exit_point,
            points=points,
            blizzards=blizzards,
            blizzard_points=set(blizzard.position for blizzard in blizzards),
            rows=len(rows) - 2,
            cols=len(rows[0]) - 2,
        )

    def valid_moves(self, position):
        return [
            point
            for point in [position] + list(position.neighbors())
            if point in self.points and point not in self.blizzard_points
        ]

    def move_blizzards(self):
        next_blizzards = [blizzard.move(self) for blizzard in self.blizzards]
        self.blizzards = next_blizzards
        self.blizzard_points = set(blizzard.position for blizzard in self.blizzards)


def get_valley():
    return Valley.from_input(utils.get_input(cast=str, delimiter='', line_delimiter='\n'))


def shortest_path(start, end, valley):
    minutes = 0
    positions = {start}

    while end not in positions:
        minutes += 1

        valley.move_blizzards()

        positions = set(itertools.chain.from_iterable(
            valley.valid_moves(position)
            for position in positions
        ))

    return minutes


@utils.part
def part_1():
    valley = get_valley()
    print(shortest_path(valley.entrance, valley.exit, valley))


@utils.part
def part_2():
    valley = get_valley()
    print(
        shortest_path(valley.entrance, valley.exit, valley) +
        shortest_path(valley.exit, valley.entrance, valley) +
        shortest_path(valley.entrance, valley.exit, valley)
    )
