import collections
import enum
import fractions

import click
import numpy as np

import utils


class Direction(enum.Enum):
    MINUS = -1
    PLUS = 1


class Sightline:
    def __init__(self, direction, slope):
        self.direction = direction
        self.slope = slope

    def __hash__(self):
        return hash((self.direction, self.slope))

    def __eq__(self, other):
        return self.direction == other.direction and self.slope == other.slope

    def __lt__(self, other):
        return self.direction.value < other.direction.value or self.slope > other.slope

    def __repr__(self):
        return 'Sightline({}, {})'.format(self.direction, self.slope)


def get_asteroids(asteroid_map):
    rows = len(asteroid_map)
    cols = len(asteroid_map[0])
    coordinates = []

    for row in range(rows):
        for col in range(cols):
            if asteroid_map[row][col] == '#':
                coordinates.append(np.array([col, row]))

    return coordinates


def sign(x):
    if x < 0:
        return -1
    return 1


def sightline(coord_1, coord_2):
    dx, dy = coord_2 - coord_1
    dx, dy = dx.item(), dy.item()

    if dx == 0:
        return Sightline(Direction(-1 * sign(dy)), float('-inf'))
    return Sightline(Direction(sign(dx)), fractions.Fraction(dy, dx))


def squared_dist(coord_1, coord_2):
    vector = coord_2 - coord_1
    return np.dot(vector, vector)


def get_sightlines(station, asteroids):
    sightlines = collections.defaultdict(list)
    for asteroid in asteroids:
        if not np.array_equal(asteroid, station):
            sightlines[sightline(station, asteroid)].append(asteroid)
    return sightlines


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    asteroid_map = utils.get_input(__file__, delimiter='', cast=str)
    asteroids = get_asteroids(asteroid_map)
    print(max(len(list(get_sightlines(station, asteroids).keys())) for station in asteroids))


@cli.command()
def part_2():
    asteroid_map = utils.get_input(__file__, delimiter='', cast=str)
    asteroids = get_asteroids(asteroid_map)

    best_station = np.array([20, 18])
    sightlines = get_sightlines(best_station, asteroids)
    sightlines = sorted(list(sightlines.items()), key=lambda item: item[0], reverse=True)

    for _, asteroids in sightlines:
        asteroids.sort(key=lambda asteroid: squared_dist(best_station, asteroid), reverse=True)

    counter = 0
    last_asteroid = None
    while counter < 200:
        _, asteroids = sightlines[counter % len(sightlines)]
        if asteroids:
            last_asteroid = asteroids.pop()
            counter += 1

    print(100 * last_asteroid[0] + last_asteroid[1])


if __name__ == '__main__':
    cli()
