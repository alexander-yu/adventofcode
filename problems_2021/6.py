import collections

import utils


def get_total_fish(days):
    timers = collections.Counter(utils.get_input()[0])

    for _ in range(days):
        birthing = timers[0]

        for i in range(8):
            timers[i] = timers[i + 1]

        timers[8] = birthing
        timers[6] += birthing

    return sum(timers.values())


@utils.part
def part_1():
    print(get_total_fish(80))


@utils.part
def part_2():
    print(get_total_fish(256))
