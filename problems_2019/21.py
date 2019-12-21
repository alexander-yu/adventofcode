import click

import utils

from problems_2019 import intcode


def commands_to_input(commands):
    return [
        ord(ch)
        for ch in
        ''.join(command + '\n' for command in commands)
    ]


def run_commands(commands):
    memory = utils.get_input(__file__)[0]
    program = intcode.Program(
        memory,
        initial_inputs=commands_to_input(commands),
        output_mode=intcode.OutputMode.BUFFER,
    )
    _, return_signal = program.run()
    assert return_signal == intcode.ReturnSignal.RETURN_AND_HALT
    for output in program.outputs:
        try:
            print(chr(output), end='')
        except ValueError:
            print(output)


@click.group()
def cli():
    pass


@cli.command()
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


@cli.command()
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


if __name__ == '__main__':
    cli()
