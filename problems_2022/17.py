import collections
import dataclasses
import itertools

from utils import Vector2D

import utils


@dataclasses.dataclass
class Shape:
    vectors: list
    bottom: int
    left: int
    right: int


SHAPES = [
    Shape(
        vectors=[Vector2D(0, 0), Vector2D(1, 0), Vector2D(2, 0), Vector2D(3, 0)],
        bottom=0,
        left=0,
        right=3,
    ),
    Shape(
        vectors=[Vector2D(0, 0), Vector2D(0, 1), Vector2D(-1, 1), Vector2D(1, 1), Vector2D(0, 2)],
        bottom=0,
        left=2,
        right=3,
    ),
    Shape(
        vectors=[Vector2D(0, 0), Vector2D(1, 0), Vector2D(2, 0), Vector2D(2, 1), Vector2D(2, 2)],
        bottom=0,
        left=0,
        right=2,
    ),
    Shape(
        vectors=[Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(0, 3)],
        bottom=0,
        left=0,
        right=0,
    ),
    Shape(
        vectors=[Vector2D(0, 0), Vector2D(0, 1), Vector2D(1, 0), Vector2D(1, 1)],
        bottom=0,
        left=0,
        right=2,
    ),
]


class Rock:
    def __init__(self, shape, height):
        self.bottom = shape.bottom
        self.left = shape.left
        self.right = shape.right

        left_shift = 2 + shape.vectors[self.bottom][0] - shape.vectors[self.left][0]

        self.points = [vector + (left_shift, height) for vector in shape.vectors]

    def shift(self, direction, tower):
        new_points = [point.shift(direction) for point in self.points]

        # If a shifted point collides with a wall, the floor, or the tower,
        # reject the shift
        if any(
            point[0] < 0 or
            point[0] > 6 or
            point[1] < 0 or
            point in tower.points for point in new_points
        ):
            return False

        self.points = new_points
        return True

    def fall(self, tower):
        return self.shift('d', tower)

    def apply_jet(self, jet, tower):
        if jet == 'l' and self.points[self.left][0] > 0:
            self.shift('l', tower)

        if jet == 'r' and self.points[self.right][0] < 6:
            self.shift('r', tower)


@dataclasses.dataclass
class Tower:
    points: set = dataclasses.field(default_factory=set)
    height: int = 0

    def add_rock(self, rock):
        self.points.update(rock.points)
        rock_height = max(point[1] for point in rock.points) + 1
        delta = rock_height - self.height

        if delta > 0:
            self.height = rock_height
            return delta

        return 0

    def __repr__(self):
        rows = []

        for y in range(self.height, -1, -1):
            row = []

            for x in range(0, 7):
                if (x, y) not in self.points:
                    row.append('.')
                else:
                    row.append('#')

            rows.append(row)

        return '\n'.join(''.join(row) for row in rows)


def get_data():
    return utils.get_input(cast=lambda j: 'l' if j == '<' else 'r', delimiter='')[0]


@utils.part
def part_1():
    data = get_data()
    shapes = itertools.cycle(SHAPES)
    jets = itertools.cycle(data)

    tower = Tower()

    for _ in range(2022):
        rock = Rock(next(shapes), tower.height + 3)

        while True:
            rock.apply_jet(next(jets), tower)
            did_fall = rock.fall(tower)

            if not did_fall:
                tower.add_rock(rock)
                break

    print(tower.height)


@dataclasses.dataclass
class Tracker:
    seen: dict = dataclasses.field(default_factory=dict)
    deltas: list = dataclasses.field(default_factory=list)
    window: collections.deque = dataclasses.field(default_factory=collections.deque)

    def track(self, time, state):
        delta = state[-1]

        # If we see a previous state, try to determine if we've detected a cycle
        # by checking that the trailing window for the last time we saw this state
        # matches the current trailing window
        if state in self.seen:
            cycle_length = time - self.seen[state]

            if list(self.window) == self.deltas[-cycle_length - 10:-cycle_length]:
                return cycle_length

        self.seen[state] = time
        self.deltas.append(delta)

        if len(self.window) >= 10:
            self.window.popleft()

        self.window.append(delta)
        return None


def get_height(num_rocks, cycle_length, deltas):
    start = len(deltas) - cycle_length
    initial, cycle = deltas[:start], deltas[start:]

    cycles = (num_rocks - start) // cycle_length
    remaining = num_rocks - cycles * cycle_length - start

    return sum(initial) + sum(cycle) * cycles + sum(cycle[:remaining])


@utils.part
def part_2():
    data = get_data()
    rocks = itertools.cycle(enumerate(SHAPES))
    jets = itertools.cycle(enumerate(data))
    tower = Tower()
    tracker = Tracker()
    num_rocks = 1000000000000
    cycle_length = None

    for t in range(num_rocks):
        rock_idx, shape = next(rocks)
        rock = Rock(shape, tower.height + 3)

        while True:
            jet_idx, jet = next(jets)

            rock.apply_jet(jet, tower)
            did_fall = rock.fall(tower)

            if not did_fall:
                delta = tower.add_rock(rock)
                state = (rock_idx, jet_idx, delta)
                cycle_length = tracker.track(t, state)
                break

        # If we've detected a cycle, stop manual rock simulation,
        # and directly calculate the final height based off of the
        # detected cycle length and the list of height deltas recorded
        # so far
        if cycle_length:
            break

    print(get_height(num_rocks, cycle_length, tracker.deltas))
