import parse

import utils


class StopException(Exception):
    pass


def get_points():
    data = utils.get_input(
        cast=lambda x: parse.parse('{:d},{:d}', x),
        delimiter=' -> ',
        line_delimiter='\n',
    )

    points = set()

    for line in data:
        for i in range(1, len(line)):
            (a, b), (c, d) = line[i - 1], line[i]

            if a == c:
                for y in range(min(b, d), max(b, d) + 1):
                    points.add(complex(a, y))
            else:
                for x in range(min(a, c), max(a, c) + 1):
                    points.add(complex(x, b))

    return points


def simulate_grain(points, threshold, threshold_is_floor=False):
    grain = complex(500, 0)

    if grain in points:
        raise StopException

    directions = [complex(0, 1), complex(-1, 1), complex(1, 1)]

    while True:
        keep_falling = False

        for direction in directions:
            new = grain + direction

            if new not in points:
                grain = new

                if not threshold_is_floor and grain.imag >= threshold:
                    raise StopException

                keep_falling = True
                break

        if not keep_falling:
            points.add(grain)
            return

        if threshold_is_floor and grain.imag == threshold - 1:
            points.add(grain)
            return


@utils.part
def part_1():
    points = get_points()
    abyss = max(point.imag for point in points)

    grains = 0
    while True:
        try:
            simulate_grain(points, abyss)
        except StopException:
            print(grains)
            return
        else:
            grains += 1


@utils.part
def part_2():
    points = get_points()
    floor = max(point.imag for point in points) + 2

    grains = 0
    while True:
        try:
            simulate_grain(points, floor, threshold_is_floor=True)
        except StopException:
            print(grains)
            return
        else:
            grains += 1
