import click

import utils

from problems_2019 import intcode


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(1)


@utils.part(cli)
def part_2():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(5)
