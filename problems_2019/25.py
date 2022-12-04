import click

import utils

from problems_2019 import intcode


def run(commands=None):
    memory = utils.get_input(__file__)[0]
    initial_inputs = intcode.commands_to_input(commands or [])
    program = intcode.Program(memory, initial_inputs=initial_inputs, output_mode=intcode.OutputMode.BUFFER)

    while True:
        _, return_signal = program.run()
        for output in program.yield_outputs():
            try:
                print(chr(output), end='')
            except ValueError:
                print(output)

        if return_signal == intcode.ReturnSignal.AWAITING_INPUT:
            # Run in interactive mode if more commands needed
            program.add_inputs(*intcode.commands_to_input([input()]))
        elif return_signal == intcode.ReturnSignal.RETURN_AND_HALT:
            return
        else:
            raise Exception(f'Unexpected return signal {return_signal}')


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    commands = [
        'south',
        'take food ration',
        'west',
        'north',
        'north',
        'east',
        'take astrolabe',
        'west',
        'south',
        'south',
        'east',
        'north',
        'east',
        'south',
        'take weather machine',
        'west',
        'take ornament',
        'east',
        'north',
        'east',
        'east',
        'east',
        'south',
    ]
    run(commands=commands)


if __name__ == '__main__':
    cli()
