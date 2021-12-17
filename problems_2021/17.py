import collections
import re

import click

import utils


TRENCH_REGEX = r'target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)'


def get_trench():
    trench = utils.get_input(__file__, delimiter=None, cast=str)[0]
    match = re.match(TRENCH_REGEX, trench)
    coords = tuple(int(match.group(i)) for i in range(1, 5))
    assert coords[0] > 0 and coords[1] > 0
    assert coords[2] < 0 and coords[3] < 0
    return coords


def triangular(n):
    return n * (n + 1) // 2


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    *_, y_0, y_1 = get_trench()

    max_y = -1

    for j in range(-y_0 + 1):
        for i in range(j):
            t_i = triangular(i)
            t_j = triangular(j)

            if y_0 <= t_i - t_j and t_i - t_j <= y_1:
                max_y = max(max_y, t_i)

    print(max_y)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    x_0, x_1, y_0, y_1 = get_trench()

    ys = set()

    for j in range(-y_0 + 1):
        for i in range(j):
            t_i = triangular(i)
            t_j = triangular(j)

            if y_0 <= t_i - t_j and t_i - t_j <= y_1:
                ys.add((i, i + j))
                ys.add((-i - 1, j - i - 1))

    xs_by_k = collections.defaultdict(list)
    zeros = set()

    for i in range(x_1 + 1):
        for j in range(i):
            t_i = triangular(i)
            t_j = triangular(j)

            if x_0 <= t_i - t_j and t_i - t_j <= x_1:
                xs_by_k[i - j - 1].append(i)
                if j == 0:
                    zeros.add(i)

    sols = set()
    for y, k in ys:
        for x in xs_by_k[k]:
            sols.add((x, y))
        if k >= min(zeros):
            for zero in zeros:
                sols.add((zero, y))

    print(len(sols))
    

if __name__ == '__main__':
    cli()
