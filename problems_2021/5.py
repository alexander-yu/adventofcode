import utils


class Vent:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.is_horizontal = begin[0] == end[0]
        self.is_vertical = begin[1] == end[1]

    def points(self):
        x_1, y_1 = self.begin
        x_2, y_2 = self.end

        x_range = range(x_1, x_2 + 1) if x_1 < x_2 else range(x_1, x_2 - 1, -1)
        y_range = range(y_1, y_2 + 1) if y_1 < y_2 else range(y_1, y_2 - 1, -1)

        if self.is_horizontal:
            return set((x_1, y) for y in y_range)
        if self.is_vertical:
            return set((x, y_1) for x in x_range)
        return set(zip(x_range, y_range))


def get_intersections(straight_only=False):
    vents = [
        Vent(
            tuple(int(val) for val in begin.split(',')),
            tuple(int(val) for val in end.split(',')),
        )
        for begin, end in
        utils.get_input(__file__, delimiter=' -> ', cast=str)
    ]

    if straight_only:
        vents = [vent for vent in vents if vent.is_horizontal or vent.is_vertical]

    intersections = set()
    num_vents = len(vents)

    for i in range(num_vents):
        for j in range(i + 1, num_vents):
            intersections |= vents[i].points() & vents[j].points()

    return intersections


@utils.part
def part_1():
    print(len(get_intersections(straight_only=True)))


@utils.part
def part_2():
    print(len(get_intersections()))
