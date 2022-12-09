from utils import Vector

import utils


def get_data():
    return utils.get_input(__file__, cast=str, delimiter=' ', line_delimiter='\n')


DIRECTIONS = {
    'R': Vector(1, 0),
    'L': Vector(-1, 0),
    'U': Vector(0, 1),
    'D': Vector(0, -1),
}


def shift_tail(head, tail):
    delta = head - tail
    dist = sum(delta.abs())

    if (
        (not all(delta)) and dist == 2 or
        dist >= 3
    ):
        tail += delta.sign()

    return tail


@utils.part
def part_1():
    data = get_data()
    head = tail = Vector(0, 0)
    positions = set([tail])

    for move in data:
        d, n = move
        n = int(n)

        for _ in range(n):
            head += DIRECTIONS[d]
            tail = shift_tail(head, tail)
            positions.add(tail)

    print(len(positions))


@utils.part
def part_2():
    data = get_data()
    knots = [Vector(0, 0) for _ in range(10)]
    positions = set([knots[-1]])

    for move in data:
        d, n = move
        n = int(n)

        for _ in range(n):
            knots[0] += DIRECTIONS[d]

            for i in range(1, 10):
                knots[i] = shift_tail(knots[i - 1], knots[i])

            positions.add(knots[-1])

    print(len(positions))
