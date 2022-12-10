import enum

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


def get_view(program):
    view = View()
    x = 0
    y = 0

    for output in program.yield_outputs():
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


@utils.part
def part_1():
    memory = utils.get_input()[0]
    program = intcode.Program(memory, output_mode=intcode.OutputMode.BUFFER)
    program.run_until_halt()
    view = get_view(program)
    view.display()

    alignment = 0
    for scaffold in view.scaffolds:
        if all(neighbor in view.scaffolds for neighbor in get_neighbors(scaffold)):
            alignment += get_alignment(scaffold)

    print(alignment)


@utils.part
def part_2():
    # Designed by inspection; look at the full path (or at least what seems like the
    # reasonable full path), and do substring matching to try and get 3 substrings that
    # generate the entire path (as long as the paths are short enough so that their
    # function length with commas is < 20); there's likely some compression algorithm
    # that can do this automatically but I don't know anything about those
    main_routine = ['A,B,A,C,A,B,C,B,C,B']
    function_a = ['R,8,L,10,L,12,R,4']
    function_b = ['R,8,L,12,R,4,R,4']
    function_c = ['R,8,L,10,R,8']
    print_output = ['n']

    commands = main_routine + function_a + function_b + function_c + print_output
    assert max(len(command) for command in commands) <= MAX_ROUTINE_SIZE

    memory = utils.get_input()[0]
    memory[0] = 2
    program = intcode.Program(
        memory,
        initial_inputs=intcode.commands_to_input(commands),
        output_mode=intcode.OutputMode.BUFFER,
    )

    output = program.run_until_halt()
    view = get_view(program)
    view.display()

    print(output)
