import itertools

from boltons import iterutils

import parse
import z3

from utils import Vector

import utils


def get_data():
    data = utils.get_input(
        cast=lambda line: parse.parse('Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', line),
        delimiter=None,
        line_delimiter='\n',
    )

    points = []

    for a, b, c, d in data:
        points.append([Vector(a, b), Vector(c, d)])

    return points


def merge_intervals(intervals):
    intervals.sort()
    merged_intervals = []

    for interval in intervals:
        if not merged_intervals or interval[0] > merged_intervals[-1][1] + 1:
            merged_intervals.append(interval)
        else:
            merged_intervals[-1][1] = max(interval[1], merged_intervals[-1][1])

    return merged_intervals


def get_excluded_intervals(data, y):
    """
    Returns a list of merged intervals that cannot contain
    the distress beacon's x value for a given y value
    """
    intervals = []

    for sensor, beacon in data:
        dist = sensor.dist(beacon)
        delta_y = abs(y - sensor[1])

        if delta_y <= dist:
            intervals.append([
                sensor[0] - (dist - delta_y),
                sensor[0] + (dist - delta_y),
            ])

    return merge_intervals(intervals)


def tuning_frequency(beacon):
    return beacon[0] * 4_000_000 + beacon[1]


@utils.part
def part_1():
    data = get_data()
    y = 2_000_000

    taken_xs = len(set(
        point
        for point in itertools.chain.from_iterable(data)
        if point[1] == y
    ))

    excluded_xs = sum(
        interval[1] - interval[0] + 1
        for interval in get_excluded_intervals(data, y)
    )

    print(excluded_xs - taken_xs)


@utils.part
def part_2_brute_force():
    """
    This solution just brute-forces the distress beacon by iterating through all rows
    and getting its excluded intervals until we find a set where [0, 4_000_000] is not entirely
    excluded
    """
    data = get_data()

    for y in range(4_000_001):
        if y % 100000 == 0:
            print(f'Y: {y}')

        excluded_intervals = get_excluded_intervals(data, y)

        if any(interval[0] <= 0 and interval[1] >= 4_000_000 for interval in excluded_intervals):
            continue

        left_interval = iterutils.first(
            excluded_intervals,
            key=lambda interval: interval[0] <= 0 and interval[1] >= 0
        )
        distress_beacon = (left_interval[1] + 1, y)

        print(tuning_frequency(distress_beacon))
        break


def z3_abs(x):
    return z3.If(x >= 0, x, -x)


@utils.part
def part_2_z3():
    solver = z3.Solver()
    x, y = z3.Int('x'), z3.Int('y')

    solver.add(x >= 0, x <= 4_000_000)
    solver.add(y >= 0, y <= 4_000_000)

    for sensor, beacon in get_data():
        dist = sensor.dist(beacon)
        solver.add(z3_abs(sensor[0] - x) + z3_abs(sensor[1] - y) > dist)

    assert solver.check() == z3.sat

    model = solver.model()
    distress_beacon = (model.evaluate(x).as_long(), model.evaluate(y).as_long())
    print(tuning_frequency(distress_beacon))
