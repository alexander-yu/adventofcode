import statistics

import click

import utils


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    positions = utils.get_input(__file__)[0]

    print(min(
        sum(
            abs(position - alignment)
            for position in positions
        )
        for alignment in range(min(positions), max(positions) + 1)
    ))


@utils.part(cli)
def part_1_median():
    # For a given list of numbers x_1, ..., x_n, the median is the value y
    # that minimizes |x_1 - y| + ... + |x_n - y|. You can prove this by seeing
    # what happens if you shift y by some epsilon, and how the sum changes depending
    # on the number of values to the left and right of y.
    positions = utils.get_input(__file__)[0]
    alignment = statistics.median(positions)
    assert alignment.is_integer()
    alignment = int(alignment)
    print(sum(abs(position - alignment) for position in positions))


@utils.part(cli)
def part_2():
    positions = utils.get_input(__file__)[0]

    print(min(
        sum(
            abs(position - alignment) * (abs(position - alignment) + 1) // 2
            for position in positions
        )
        for alignment in range(min(positions), max(positions) + 1)
    ))


if __name__ == '__main__':
    cli()
