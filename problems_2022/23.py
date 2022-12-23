import collections
import dataclasses

from utils import Vector2D

import utils


DIRECTIONS = Vector2D.directions(include_diagonals=True)


def get_elves():
    elves = set()

    for i, row in enumerate(utils.get_input(cast=str, delimiter='')[::-1]):
        for j, value in enumerate(row):
            if value == '#':
                elves.add(Vector2D(j, i))

    return elves


def propose_moves(rules, elves):
    moves = {}

    for elf in elves:
        neighbors = {vector: elf + vector for vector in DIRECTIONS}

        if elves.intersection(neighbors.values()):
            for vectors, direction in rules:
                if all(neighbors[vector] not in elves for vector in vectors):
                    moves[elf] = elf.shift(direction)
                    break

    rules.rotate(-1)
    return moves


def execute_moves(elves, moves):
    new_elves = set()
    num_moves = 0
    destinations = collections.defaultdict(list)

    for elf, destination in moves.items():
        destinations[destination].append(elf)

    for elf in elves:
        if (destination := moves.get(elf)) and len(destinations[destination]) == 1:
            new_elves.add(destination)
            num_moves += 1
            continue

        new_elves.add(elf)

    return new_elves, num_moves


@dataclasses.dataclass
class Boundary:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    @staticmethod
    def from_elves(elves):
        return Boundary(
            min_x=min(elf[0] for elf in elves),
            max_x=max(elf[0] for elf in elves),
            min_y=min(elf[1] for elf in elves),
            max_y=max(elf[1] for elf in elves),
        )

    def __abs__(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)


def spread_out(max_rounds=None):
    elves = get_elves()
    rules = collections.deque([
        ({vector for vector in DIRECTIONS if vector[1] == 1}, 'N'),
        ({vector for vector in DIRECTIONS if vector[1] == -1}, 'S'),
        ({vector for vector in DIRECTIONS if vector[0] == -1}, 'W'),
        ({vector for vector in DIRECTIONS if vector[0] == 1}, 'E'),
    ])
    rounds = 0

    while True:
        moves = propose_moves(rules, elves)
        elves, num_moves = execute_moves(elves, moves)
        rounds += 1

        if not num_moves or rounds == max_rounds:
            return elves, rounds


@utils.part
def part_1():
    elves, _ = spread_out(max_rounds=10)
    print(abs(Boundary.from_elves(elves)) - len(elves))


@utils.part
def part_2():
    _, rounds = spread_out()
    print(rounds)
