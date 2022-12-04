import itertools

import click
import z3

import utils


# Rules determined by manually inspecting the logic of the given program.
# Note that each section after an `inp w` tends to follow one of two patterns.
#
# The final expression for one type of section S_i increases the value of z always,
# due to the fact that w_i is always a digit from 1-9, whereas the other type of section
# either conditionally increases z (and would include w_i as part of it) or decreases
# z, and the condition is always based on a comparison between two inputs (e.g. w_2 - w_3 = 8).
#
# Note that there are 7 sections that always increase z by roughly a factor of 26, and 7 sections
# that conditionally decrease or increase z by a factor of 26. Another way to think of it is that
# z is acting as a base-26 stack of w_i + offset_i expressions.
#
# In order for a number to be valid, z must be 0 at the end (i.e. the stack must be empty), meaning
# that we must always satisfy every condition that causes a conditional decrease. Below, we have a
# derived list of the conditions that must be satisfied.
RULES = {
    # (w_2, w_3): w_2 - w_3 = -8
    (2, 3): -8,
    # (w_1, w_4): w_1 - w_4 = 2
    (1, 4): 2,
    # (w_5, w_6): w_5 - w_6 = 8
    (5, 6): 8,
    # (w_0, w_7): w_0 - w_7 = -2
    (0, 7): -2,
    # (w_9, w_10): w_9 - w_10 = 6
    (9, 10): 6,
    # (w_11, w_12): w_11 - w_12 = 1
    (11, 12): 1,
    # (w_8, w_13): w_8 - w_13 = 4
    (8, 13): 4,
}


def get_valid_pairs(delta):
    return [(i, i - delta) for i in range(1, 10) if 1 <= i - delta <= 9]


def valid_numbers():
    pairs = list(RULES.keys())
    valid_pairs = [get_valid_pairs(RULES[pair]) for pair in pairs]
    valid_numbers = []

    for pair_values in itertools.product(*valid_pairs):
        assignments = sorted(
            itertools.chain.from_iterable(
                zip(pair, pair_value)
                for pair, pair_value in zip(pairs, pair_values)
            ),
            key=lambda assignment: assignment[0],
        )
        number = int(''.join(str(assignment[1]) for assignment in assignments))
        valid_numbers.append(number)

    return valid_numbers


def valid_numbers_z3(optimize_method):
    digits = z3.IntVector('digits', 14)
    optimizer = z3.Optimize()
    number = 0

    for i in range(14):
        optimizer.add(1 <= digits[i], digits[i] <= 9)
        number = 10 * number + digits[i]

    for (i, j), delta in RULES.items():
        optimizer.add(digits[i] - digits[j] == delta)

    getattr(optimizer, optimize_method)(number)
    assert optimizer.check() == z3.sat
    return optimizer.model().eval(number)


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    print(max(valid_numbers()))


@utils.part(cli)
def part_2():
    print(min(valid_numbers()))


@utils.part(cli)
def part_1_z3():
    print(valid_numbers_z3('maximize'))


@utils.part(cli)
def part_2_z3():
    print(valid_numbers_z3('minimize'))


if __name__ == '__main__':
    cli()
