import utils

from problems_2019 import intcode


@utils.part
def part_1():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(1)


@utils.part
def part_2():
    memory = utils.get_input(__file__)[0]
    intcode.Program(memory).run(5)
