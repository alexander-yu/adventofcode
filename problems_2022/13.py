import ast
import functools
import itertools

from boltons import iterutils

import utils


def get_packets():
    return utils.get_input(cast=ast.literal_eval, delimiter='\n', line_delimiter='\n\n')


def compare(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return utils.sign(x - y)

    if isinstance(x, int):
        return compare([x], y)

    if isinstance(y, int):
        return compare(x, [y])

    return (
        # Run through lists and return the first non-zero comparison result.
        # If all elements compare as equal, just compare it based on which list
        # still has elements remaining.
        iterutils.first(
            compare(xi, yi)
            for xi, yi in zip(x, y)
        )
        or compare(len(x), len(y))
    )


@utils.part
def part_1():
    packets = get_packets()
    print(sum(
        i + 1
        for i, (x, y) in enumerate(packets)
        if compare(x, y) < 0
    ))


@utils.part
def part_2():
    divider_1, divider_2 = [[2]], [[6]]
    packets = list(itertools.chain.from_iterable(get_packets())) + [divider_1, divider_2]

    packets.sort(key=functools.cmp_to_key(compare))

    i1 = packets.index(divider_1) + 1
    i2 = packets.index(divider_2) + 1

    print(i1 * i2)
