import click

import utils


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    depths = utils.get_input(__file__, delimiter=None)

    increases = sum(
        depths[i] - depths[i - 1] > 0
        for i in range(1, len(depths))
    )

    print(increases)


@utils.part(cli)
def part_2():
    depths = utils.get_input(__file__, delimiter=None)

    increases = sum(
        depths[i] - depths[i - 3] > 0
        for i in range(3, len(depths))
    )

    print(increases)
