import dataclasses
import re

import parse

import utils


@dataclasses.dataclass
class Move:
    size: int
    start: list
    end: list


def get_initial_stacks(stack_rows, stack_labels):
    num_stacks = len(re.findall(r'\d+', stack_labels))
    stacks = [[] for _ in range(num_stacks)]

    for stack_row in reversed(stack_rows):
        for idx, crate in enumerate(stack_row[1::4]):
            if crate.isalpha():
                stacks[idx].append(crate)

    return stacks


def get_moves(stacks, moves):
    for move in moves:
        size, start, end = parse.parse('move {:d} from {:d} to {:d}', move)
        yield Move(size, stacks[start - 1], stacks[end - 1])


def get_data():
    stack_data, moves = utils.get_input(__file__, cast=str, delimiter='\n', line_delimiter='\n\n')

    stacks = get_initial_stacks(stack_data[:-1], stack_data[-1])
    moves = get_moves(stacks, moves)

    return stacks, moves


def exec_move(move, crane=False):
    crates = []

    for _ in range(move.size):
        crates.append(move.start.pop())

    if crane:
        crates = crates[::-1]

    move.end.extend(crates)


def run(crane=False):
    stacks, moves = get_data()

    for move in moves:
        exec_move(move, crane=crane)

    print(''.join(stack[-1] for stack in stacks))


@utils.part
def part_1():
    run()


@utils.part
def part_2():
    run(crane=True)
