import click

import utils

from problems_2019 import intcode


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(1)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(5)


if __name__ == '__main__':
    cli()
