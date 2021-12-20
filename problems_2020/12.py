import re

import click
import numpy as np

import utils


INSTRUCTION_REGEX = r'(?P<action>[A-Z])(?P<value>\d+)'
WAYPOINT_DELTA = np.array([
    [10],
    [1],
])

DIRECTION_ACTIONS = {
    'N': utils.Direction.NORTH,
    'E': utils.Direction.EAST,
    'S': utils.Direction.SOUTH,
    'W': utils.Direction.WEST,
}

ROTATION_ACTIONS = {
    'L': 1,
    'R': -1,
}


class Ship:
    def __init__(self, waypoint=False):
        self.position = np.copy(utils.ORIGIN)
        self.direction = utils.DIRECTIONS[utils.Direction.EAST]
        self.waypoint_delta = WAYPOINT_DELTA if waypoint else None
        self.waypoint = waypoint

    def _move(self, direction, distance, waypoint=False):
        vector = direction * distance

        if waypoint:
            self.waypoint_delta += vector
        else:
            self.position += vector

    def _rotate(self, degrees, waypoint=False):
        rotation = utils.ROTATIONS_2D[(degrees // 90) % 4]

        if waypoint:
            self.waypoint_delta = np.dot(rotation, self.waypoint_delta)
        else:
            self.direction = np.dot(rotation, self.direction)

    def execute(self, action, value):
        if action in DIRECTION_ACTIONS:
            direction = utils.DIRECTIONS[DIRECTION_ACTIONS[action]]
            self._move(direction, value, waypoint=self.waypoint)
        elif action in ROTATION_ACTIONS:
            rotation = ROTATION_ACTIONS[action]
            self._rotate(rotation * value, waypoint=self.waypoint)
        else:
            assert action == 'F'
            if self.waypoint:
                self._move(self.waypoint_delta, value)
            else:
                self._move(self.direction, value)


def parse_instruction(string):
    match = re.fullmatch(INSTRUCTION_REGEX, string)
    return match.group('action'), int(match.group('value'))


def manhattan_distance(x, y):
    return np.abs(x - y).sum()


def navigate_ship(ship):
    for instruction in utils.get_input(__file__, delimiter=None, cast=str):
        action, value = parse_instruction(instruction)
        ship.execute(action, value)

    return ship.position


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    ship = Ship()
    position = navigate_ship(ship)
    print(manhattan_distance(utils.ORIGIN, position))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    ship = Ship(waypoint=True)
    position = navigate_ship(ship)
    print(manhattan_distance(utils.ORIGIN, position))


if __name__ == '__main__':
    cli()
