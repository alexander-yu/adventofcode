import click

import utils

from problems_2019 import intcode


def run():
    memory = utils.get_input(__file__)[0]
    program = intcode.Program(memory, output_mode=intcode.OutputMode.BUFFER)
    while True:
        _, return_signal = program.run()
        for output in program.yield_outputs():
            try:
                print(chr(output), end='')
            except ValueError:
                print(output)

        if return_signal == intcode.ReturnSignal.AWAITING_INPUT:
            program.add_inputs(*intcode.commands_to_input([input()]))
        elif return_signal == intcode.ReturnSignal.RETURN_AND_HALT:
            return
        else:
            raise Exception(f'Unexpected return signal {return_signal}')


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    run()


if __name__ == '__main__':
    cli()
