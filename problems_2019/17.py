import collections
import enum
import itertools

import click
import numpy as np

import utils

from problems_2019 import intcode


EMPTY = '.'
NEWLINE = '\n'
SCAFFOLD = '#'
CURSORS = ['^', '>', '<', 'V', 'X']
MAX_ROUTINE_SIZE = 20
VECTORS = [
    np.array([0, 1]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([-1, 0]),
]


class Function(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'


class Rotation(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'


class View:
    def __init__(self):
        self.points = {}
        self.scaffolds = set()
        self.width = 0
        self.height = 0

    def display(self):
        for y in range(0, -1 * self.height, -1):
            for x in range(0, self.width):
                print(self.points.get((x, y), ''), end='')

        print()


def get_neighbors(point):
    return [tuple(np.array(point) + vector) for vector in VECTORS]


def get_alignment(point):
    return abs(point[0]) * abs(point[1])


def get_main_routine(functions):
    routine = [
        ord(ch)
        for ch in
        ','.join(function.value for function in functions) + '\n'
    ]
    assert len(routine) <= MAX_ROUTINE_SIZE + 1  # Add 1 to account for newline
    return routine


def get_function(movements):
    function = [
        ord(ch)
        for ch in
        ','.join(
            movement.value if isinstance(movement, Rotation) else str(movement)
            for movement in movements
        ) + '\n'
    ]
    assert len(function) <= MAX_ROUTINE_SIZE + 1  # Add 1 to account for newline
    return function


def get_view(outputs):
    view = View()
    x = 0
    y = 0

    while outputs:
        output = outputs.popleft()
        output = chr(output)
        view.points[(x, y)] = output

        if output == SCAFFOLD:
            view.scaffolds.add((x, y))

        if output == NEWLINE:
            view.width = max(view.width, x + 1)
            x = 0
            y -= 1
        elif output in CURSORS + [SCAFFOLD, EMPTY]:
            x += 1

    view.height = abs(y)
    return view


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    memory = utils.get_input(__file__)[0]
    program = intcode.Program(memory, output_mode=intcode.OutputMode.BUFFER)
    _, return_signal = program.run()
    assert return_signal == intcode.ReturnSignal.RETURN_AND_HALT

    view = get_view(program.outputs)
    view.display()

    alignment = 0
    for scaffold in view.scaffolds:
        if all(neighbor in view.scaffolds for neighbor in get_neighbors(scaffold)):
            alignment += get_alignment(scaffold)

    print(alignment)


@cli.command()
def part_2():
    # Designed by inspection; look at the full path (or at least what seems like the
    # reasonable full path), and do substring matching to try and get 3 substrings that
    # generate the entire path (as long as the paths are short enough so that their
    # function length with commas is < 20); there's likely some compression algorithm
    # that can do this automatically but I don't know anything about those
    main_routine = get_main_routine([
        Function.A,
        Function.B,
        Function.A,
        Function.C,
        Function.A,
        Function.B,
        Function.C,
        Function.B,
        Function.C,
        Function.B,
    ])
    function_a = get_function([
        Rotation.RIGHT,
        8,
        Rotation.LEFT,
        10,
        Rotation.LEFT,
        12,
        Rotation.RIGHT,
        4,
    ])
    function_b = get_function([
        Rotation.RIGHT,
        8,
        Rotation.LEFT,
        12,
        Rotation.RIGHT,
        4,
        Rotation.RIGHT,
        4,
    ])
    function_c = get_function([
        Rotation.RIGHT,
        8,
        Rotation.LEFT,
        10,
        Rotation.RIGHT,
        8,
    ])

    function_inputs = main_routine + function_a + function_b + function_c

    memory = utils.get_input(__file__)[0]
    memory[0] = 2
    program = intcode.Program(
        memory,
        initial_inputs=function_inputs + [ord('n'), ord('\n')],
        output_mode=intcode.OutputMode.BUFFER,
    )

    output, return_signal = program.run()
    assert return_signal == intcode.ReturnSignal.RETURN_AND_HALT

    view = get_view(program.outputs)
    view.display()

    print(output)


if __name__ == '__main__':
    cli()
