import click

import utils

from problems_2019 import intcode


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    memory = utils.get_input(__file__)[0]
    beam = 0
    points = {}
    for x in range(50):
        for y in range(50):
            program = intcode.Program(memory, initial_inputs=[x, y], output_mode=intcode.OutputMode.BUFFER)
            output, return_signal = program.run()
            assert return_signal == intcode.ReturnSignal.RETURN_AND_HALT
            points[(x, y)] = output
            beam += output

    print(beam)
    for y in range(50):
        for x in range(50):
            output = '#' if points[(x, y)] else '.'
            print(output, end='')

        print()

@cli.command()
def part_2():
    pass


if __name__ == '__main__':
    cli()
