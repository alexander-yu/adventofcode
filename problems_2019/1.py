import itertools

import utils


def fuel(n):
    return max(n // 3 - 2, 0)


def fuel_total(n):
    total = 0
    while n:
        n = fuel(n)
        total += n

    return total


@utils.part
def part_1():
    module_masses = itertools.chain.from_iterable(utils.get_input(__file__))
    print(sum(fuel(module_mass) for module_mass in module_masses))


@utils.part
def part_2():
    module_masses = itertools.chain.from_iterable(utils.get_input(__file__))
    print(sum(fuel_total(module_mass) for module_mass in module_masses))
