import click

import utils


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    positions = utils.get_input(__file__)[0]

    print(min(
        sum(
            abs(position - alignment)
            for position in positions
        )
        for alignment in range(min(positions), max(positions) + 1)
    ))


@cli.command()
@utils.part(__name__, 2)
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
