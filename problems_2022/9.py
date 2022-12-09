import utils


def get_data():
    return utils.get_input(__file__, cast=str, delimiter=' ', line_delimiter='\n')


vs = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def shift_tail(head, tail):
    dx, dy = utils.subtract_vector(head, tail)
    dist = abs(dx) + abs(dy)

    if (
        (not dx or not dy) and dist == 2 or
        dist >= 3
    ):
        vector = (utils.sign(dx), utils.sign(dy))
        return utils.add_vector(tail, vector)

    return tail


@utils.part
def part_1():
    data = get_data()

    tail = (0, 0)
    head = (0, 0)
    positions = set([tail])

    for move in data:
        d, n = move
        n = int(n)

        for _ in range(n):
            v = vs[d]
            head = utils.add_vector(head, v)
            tail = shift_tail(head, tail)
            positions.add(tail)

    print(len(positions))


@utils.part
def part_2():
    data = get_data()

    knots = [(0, 0) for _ in range(10)]
    positions = set([(0, 0)])

    for move in data:
        d, n = move
        n = int(n)

        for _ in range(n):
            v = vs[d]
            knots[0] = utils.add_vector(knots[0], v)

            for i in range(1, 10):
                knots[i] = shift_tail(knots[i - 1], knots[i])

            positions.add(knots[-1])

    print(len(positions))
