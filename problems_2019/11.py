import enum

import numpy as np

import utils

from problems_2019 import intcode


class Color(enum.Enum):
    BLACK = 0
    WHITE = 1


class Rotation(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


ROTATIONS = {
    Direction.UP: {
        Rotation.LEFT: Direction.LEFT,
        Rotation.RIGHT: Direction.RIGHT,
    },
    Direction.DOWN: {
        Rotation.LEFT: Direction.RIGHT,
        Rotation.RIGHT: Direction.LEFT,
    },
    Direction.LEFT: {
        Rotation.LEFT: Direction.DOWN,
        Rotation.RIGHT: Direction.UP,
    },
    Direction.RIGHT: {
        Rotation.LEFT: Direction.UP,
        Rotation.RIGHT: Direction.DOWN,
    },
}

VECTORS = {
    Direction.UP: np.array([0, 1]),
    Direction.DOWN: np.array([0, -1]),
    Direction.LEFT: np.array([-1, 0]),
    Direction.RIGHT: np.array([1, 0]),
}

PAINT = {
    Color.BLACK: '.',
    Color.WHITE: '#',
}


class Panel:
    def __init__(self, position, color=Color.BLACK):
        self.position = position
        self.color = color


def move(position, direction, rotation):
    new_direction = ROTATIONS[direction][rotation]
    vector = VECTORS[new_direction]
    new_position = tuple(np.array(position) + vector)
    return new_position, new_direction


def paint(program_memory, initial_position=(0, 0), initial_direction=Direction.UP, initial_color=Color.BLACK):
    curr_panel = Panel(initial_position, color=initial_color)
    curr_direction = initial_direction
    painted_panels = {}
    program = intcode.Program(program_memory, output_mode=intcode.OutputMode.PIPE)

    while True:
        program.add_inputs(curr_panel.color.value)
        new_color, return_signal = program.run()
        if return_signal == intcode.ReturnSignal.RETURN_AND_HALT:
            break

        curr_panel.color = Color(new_color)
        painted_panels[curr_panel.position] = curr_panel

        rotation, return_signal = program.run()
        new_position, new_direction = move(curr_panel.position, curr_direction, Rotation(rotation))
        new_panel = painted_panels.get(new_position, Panel(new_position))

        curr_panel = new_panel
        curr_direction = new_direction

        assert return_signal == intcode.ReturnSignal.RETURN_AND_WAIT

    return painted_panels


def display(painted_panels):
    min_width = min(position[0] for position in painted_panels)
    max_width = max(position[0] for position in painted_panels)
    min_height = min(position[1] for position in painted_panels)
    max_height = max(position[1] for position in painted_panels)

    width = max_width - min_width + 1
    height = max_height - min_height + 1

    hull = []
    for i in range(height):
        line = []
        hull.append(line)

        for j in range(width):
            position = (min_width + j, min_height + i)
            panel = painted_panels.get(position, Panel(position))
            line.append(PAINT[panel.color])

    return hull[::-1]


@utils.part
def part_1():
    program_memory = utils.get_input()[0]
    print(len(paint(program_memory)))


@utils.part
def part_2():
    program_memory = utils.get_input()[0]
    hull = display(paint(program_memory, initial_color=Color.WHITE))
    for line in hull:
        print(''.join(line))
