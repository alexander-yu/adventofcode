import utils

from problems_2019 import intcode


def run_commands(commands):
    memory = utils.get_input()[0]
    program = intcode.Program(
        memory,
        initial_inputs=intcode.commands_to_input(commands),
        output_mode=intcode.OutputMode.BUFFER,
    )
    program.run_until_halt()
    for output in program.yield_outputs():
        try:
            print(chr(output), end='')
        except ValueError:
            print(output)


@utils.part
def part_1():
    run_commands([
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'AND D T',
        'OR T J',
        'WALK',
    ])


@utils.part
def part_2():
    run_commands([
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'AND D T',
        'OR T J',
        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J',
        'RUN',
    ])
