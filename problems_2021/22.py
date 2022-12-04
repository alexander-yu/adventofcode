import collections
import dataclasses
import math
import re

import click

import utils


INTERVAL_REGEX = r'[xyz]=(-?\d+)..(-?\d+)'


@dataclasses.dataclass(frozen=True)
class Interval:
    lower: int
    upper: int

    def __len__(self):
        return self.upper - self.lower

    def __and__(self, other):
        if other.upper < self.lower or self.upper < other.lower:
            return Interval(0, 0)

        return Interval(max(self.lower, other.lower), min(self.upper, other.upper))


@dataclasses.dataclass(frozen=True)
class Cuboid:
    x_interval: Interval
    y_interval: Interval
    z_interval: Interval

    def _intervals(self):
        return [self.x_interval, self.y_interval, self.z_interval]

    def __len__(self):
        return math.prod(len(interval) for interval in self._intervals())

    def __and__(self, other):
        return Cuboid(
            self.x_interval & other.x_interval,
            self.y_interval & other.y_interval,
            self.z_interval & other.z_interval,
        )


def get_cuboid(cuboid_str):
    intervals = []
    for interval in utils.parse(cuboid_str, cast=str)[0]:
        match = re.match(INTERVAL_REGEX, interval)
        intervals.append(Interval(
            int(match.group(1)),
            int(match.group(2)) + 1,
        ))

    return Cuboid(*intervals)


def get_steps():
    steps = utils.get_input(__file__, delimiter=' ', cast=str)
    return [(step[0], get_cuboid(step[1])) for step in steps]


def run_steps(steps, initial_area=None):
    cuboid_signs = collections.Counter()

    for state, next_cuboid in steps:
        new_sign = 1 if state == 'on' else -1

        if initial_area:
            next_cuboid &= initial_area
            if not next_cuboid:
                continue

        updates = collections.Counter()
        for cuboid, sign in cuboid_signs.items():
            intersection = cuboid & next_cuboid
            if intersection:
                updates[intersection] -= sign

        if new_sign == 1:
            updates[next_cuboid] += new_sign

        cuboid_signs.update(updates)

    return sum(len(cuboid) * sign for cuboid, sign in cuboid_signs.items())


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    steps = get_steps()
    initial_area = Cuboid(
        Interval(-50, 51),
        Interval(-50, 51),
        Interval(-50, 51),
    )
    print(run_steps(steps, initial_area=initial_area))


@utils.part(cli)
def part_2():
    steps = get_steps()
    print(run_steps(steps))


if __name__ == '__main__':
    cli()
