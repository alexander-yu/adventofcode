import click

import utils

from problems_2019 import intcode


def get_output(memory, x, y):
    program = intcode.Program(memory, initial_inputs=[x, y], output_mode=intcode.OutputMode.BUFFER)
    output, return_signal = program.run()
    assert return_signal == intcode.ReturnSignal.RETURN_AND_HALT
    return output


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


@cli.command()
def part_2():
    memory = utils.get_input(__file__)[0]
    # Start from here because there is an empty initial stem of the beam
    x, y, = 5, 4
    assert get_output(memory, x, y) == 1

    while True:
        y += 1
        # Move right until we've reached the next top-left corner (since the beam moves right)
        while not get_output(memory, x, y):
            x += 1

        if get_output(memory, x + 99, y - 99):
            print(x, y - 99)
            break


if __name__ == '__main__':
    cli()
