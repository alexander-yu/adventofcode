import utils


def get_moves():
    return utils.get_input(format='{} {:d}')


def shift_knot(parent, knot):
    delta = parent - knot

    if any(d >= 2 for d in delta.abs()):
        knot += delta.sign()

    return knot


def get_tail_positions(num_knots):
    moves = get_moves()
    knots = [utils.ORIGIN for _ in range(num_knots)]
    positions = set([knots[-1]])

    for d, n in moves:
        for _ in range(n):
            knots[0] = knots[0].shift(d)

            for i in range(1, len(knots)):
                knots[i] = shift_knot(knots[i - 1], knots[i])

            positions.add(knots[-1])

    return len(positions)


@utils.part
def part_1():
    print(get_tail_positions(2))


@utils.part
def part_2():
    print(get_tail_positions(10))
