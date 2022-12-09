import utils


def get_moves():
    return utils.get_input(__file__, format='{} {:d}', line_delimiter='\n')


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
    data = get_moves()
    head = tail = utils.ORIGIN
    positions = set([tail])

    for move in data:
        d, n = move

        for _ in range(n):
            head += utils.DIRECTIONS[d]
            tail = shift_tail(head, tail)
            positions.add(tail)

    print(len(positions))


@utils.part
def part_2():
    data = get_moves()
    knots = [utils.ORIGIN for _ in range(10)]
    positions = set([knots[-1]])

    for move in data:
        d, n = move

        for _ in range(n):
            knots[0] += utils.DIRECTIONS[d]

            for i in range(1, 10):
                knots[i] = shift_tail(knots[i - 1], knots[i])

            positions.add(knots[-1])

    print(len(positions))
