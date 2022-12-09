import utils


def get_moves():
    return utils.get_input(__file__, format='{} {:d}', line_delimiter='\n')


def shift_knot(parent, knot):
    delta = parent - knot

    if any(d >= 2 for d in delta.abs()):
        knot += delta.sign()

    return knot


def get_tail_positions(num_knots):
    data = get_moves()
    knots = [utils.ORIGIN for _ in range(num_knots)]
    positions = set([knots[-1]])

    for move in data:
        d, n = move

        for _ in range(n):
            knots[0] += utils.DIRECTIONS[d]

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
