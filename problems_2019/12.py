import functools
import itertools
import math
import re

import click
import numpy as np

import utils


# This matches against input of the form <x=int, y=int, z=int>, where "int" can be
# any integer, positive or negative, and captures each of the coordinates in a group
# whose name corresponds with the coordinate name
MOON_TEMPLATE = r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>'


class Moon:
    def __init__(self, position):
        self.velocity = np.zeros(3, dtype=int)
        self.position = position

    def apply_velocity(self, axis=None):
        if axis is None:
            self.position += self.velocity
        else:
            self.position[axis] += self.velocity[axis]

    def energy(self):
        return int(np.linalg.norm(self.position, ord=1) * np.linalg.norm(self.velocity, ord=1))

    def __repr__(self):
        return f'pos={self.position}, vel={self.velocity}'


def parse_moon(moon):
    match = re.match(MOON_TEMPLATE, moon)
    assert match

    return Moon(np.array([
        int(match.group('x')),
        int(match.group('y')),
        int(match.group('z')),
    ]))


def get_gravity(moon_1, moon_2, axis=None):
    if axis is None:
        position_1, position_2 = moon_1.position, moon_2.position
    else:
        position_1, position_2 = moon_1.position[axis], moon_2.position[axis]

    # If coordinate_1 > coordinate_2, then coordinate_1 must change by -1; conversely,
    # if coordinate_1 < coordinate_2, then coordinate_1 must change by +1, and finally,
    # if coordinate_1 == coordinate_2, then coordinate_1 should not change. This can be
    # succinctly evaluated as the below expression:
    gravity_1 = 2 * (position_1 < position_2) - 1 + (position_1 == position_2)
    gravity_2 = -1 * gravity_1
    return gravity_1, gravity_2


def apply_gravity(moon_1, moon_2, axis=None):
    gravity_1, gravity_2 = get_gravity(moon_1, moon_2, axis=axis)

    if axis is None:
        moon_1.velocity += gravity_1
        moon_2.velocity += gravity_2
    else:
        moon_1.velocity[axis] += gravity_1
        moon_2.velocity[axis] += gravity_2


def simulate_motion(moons, steps, axis=None):
    for _ in range(steps):
        for moon_1, moon_2 in itertools.combinations(moons, 2):
            apply_gravity(moon_1, moon_2, axis=axis)

        for moon in moons:
            moon.apply_velocity(axis=axis)


def get_moons():
    return [
        parse_moon(moon)
        for moon in
        utils.get_input(__file__, delimiter=None, cast=str)
    ]


def get_axis_cycle(axis):
    moons = get_moons()
    initial_coordinates = np.array([moon.position[axis] for moon in moons])
    initial_velocity = np.zeros(len(moons))
    steps = 0

    while True:
        simulate_motion(moons, 1, axis=axis)
        steps += 1

        coordinates = np.array([moon.position[axis] for moon in moons])
        velocity = np.array([moon.velocity[axis] for moon in moons])

        if np.array_equal(coordinates, initial_coordinates) and np.array_equal(velocity, initial_velocity):
            break

    return steps


def lcm(a, b):
    return a * b // math.gcd(a, b)


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    moons = get_moons()
    simulate_motion(moons, 1000)
    print(sum(moon.energy() for moon in moons))


@utils.part(cli)
def part_2():
    print(functools.reduce(lcm, [get_axis_cycle(axis) for axis in [0, 1, 2]]))
