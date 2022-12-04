import collections
import itertools
import math
import re

import click

import utils


TRENCH_REGEX = r'target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)'


def get_trench():
    trench = utils.get_input(__file__, delimiter=None, cast=str)[0]
    match = re.match(TRENCH_REGEX, trench)
    coords = tuple(int(match.group(i)) for i in range(1, 5))
    assert coords[0] > 0 and coords[1] > 0
    assert coords[2] < 0 and coords[3] < 0
    return coords


def triangular(n):
    return n * (n + 1) // 2


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    *_, y_0, _ = get_trench()

    # Note that if y is the initial vertical velocity, and we assume trench is in 3rd quadrant,
    # meaning that we must have k > y, then the total gain will be
    # y + y - 1 + ... + 0 - 1 - ... - (k - y) = T_y - T_{k - y},
    # where k is the number of steps and T_n represents the nth triangular number.
    # We also assume for this part that y > 0.
    #
    # The max height will be T_y, and since T_y is monotonically increasing in y,
    # we really just need to find the max y satisfying y_0 <= T_y - T_{k - y} <= y_1
    # for some k.
    #
    # The inequalities are equivalent to T_{k - y} <= T_y + (-y_0) and
    # T_y + (-y_1) <= T_{k - y}. Note that T_{k - y} > T_y since we assume trench is 3rd quadrant,
    # or in other words, k - y > y. Substituting k - y with some l, this is equivalent to
    # T_y < T_l <= T_y + (-y_0) and T_y + (-y_1) <= T_l, where y < l.
    #
    # By inspection, we can see that y <= -y_0 - 1, since if y >= -y_0, then we can see that
    # T_l - T_y >= l > y >= -y_0, a contradiction. y = -y_0 - 1 satisfies the inequalities too,
    # if we set l = -y_0, so -y_0 - 1 is the max possible y.
    print(triangular(-y_0 - 1))


@cli.command
@utils.part
def part_2():
    x_0, x_1, y_0, y_1 = get_trench()

    # Create a set of valid initial y values + step numbers for each y.
    ys = set()

    # If y >= 0, then net gain will be T_y - T_{k - y}, where we note that k - y <= -y_0, using the same
    # logic as above, since k - y <= T_{k - y} - T_y <= -y_0. Setting i = y and j = k - y yields k = i + j
    # and y = i.
    #
    # If y < 0, then net gain will be T_{-y - 1} - T_{k - y}. Note that we must have
    # k - y <= T_{k - y} - T_{-y - 1} <= -y_0, similarly as above. Setting i = -y - 1 and j = k - y yields
    # k = j - i - 1 and y = -i - 1.
    for j in range(-y_0 + 1):
        for i in range(j):
            t_i = triangular(i)
            t_j = triangular(j)

            if y_0 <= t_i - t_j <= y_1:
                ys.add((i, i + j))
                ys.add((-i - 1, j - i - 1))

    # Create a mapping of step number k -> x values that can reach trench boundaries in k steps.
    # This does not properly account for the situation where if the probe has started falling vertically
    # within trench boundaries, we can add infinitely many steps (since the x value doesn't change).
    #
    # We also keep a set of step numbers where this scenario is possible.
    xs_by_steps = collections.defaultdict(list)
    verticals = set()

    for i in range(x_1 + 1):
        for j in range(i):
            t_i = triangular(i)
            t_j = triangular(j)

            # Similary to above, we know that x > 0 but total horizontal gain will never go negative.
            # So the net gain is x + x - 1 + ... + x - k = T_x - T_{x - k - 1} if k < x, else T_x.
            # Setting i = x and j = x - k - 1 yields k = i - j - 1 and x = i.
            # Note if x - k - 1 = j = 0, then this corresponds to a flight path where the probe has
            # started falling vertically. Keep track of this scenario.
            if x_0 <= t_i - t_j <= x_1:
                xs_by_steps[i - j - 1].append(i)
                if j == 0:
                    verticals.add(i)

    # For each valid (y, k), find all valid x for that k. If k >= min(verticals), we encounter a scenario
    # where it could actually just be falling vertically. xs_by_steps does not automatically track this,
    # so we need to manually check and add these scenarios.
    velocities = set()
    for y, steps in ys:
        for x in xs_by_steps[steps]:
            velocities.add((x, y))
        if steps >= min(verticals):
            for vertical in verticals:
                velocities.add((vertical, y))

    print(len(velocities))


def get_int_range(a, b):
    return range(math.ceil(a), math.floor(b) + 1)


def get_valid_y(steps, y_0, y_1):
    # Note that for a given y and steps k, the net gain will be
    # y + (y - 1) + ... + (y - k) = (k + 1) * y - k * (k + 1)/2, which we'll call f_k(y).
    #
    # Solving the inequality y_0 <= f_k(y) <= y_1, where y_0 < y_1 < 0 <= k yields
    # y_0/(k + 1) + k/2 <= y <= y_1/(k + 1) + k/2.
    return get_int_range(
        y_0/(steps + 1) + steps/2,
        y_1/(steps + 1) + steps/2,
    )


def inverse_triangular(n):
    return (math.sqrt(8 * n + 1) - 1) / 2


def get_valid_x(steps, x_0, x_1):
    # Note that for a given x and steps k, the net gain will be
    # x + x - 1 + ... + x - k = (k + 1) * x - k * (k + 1)/2 if k <= x
    # else T_x = x * (x + 1) / 2. We'll call the former expression f_k(x).
    #
    # Now let S(x) be the inverse of T_x = x * (x + 1) / 2, which can be written as
    # (sqrt(8x + 1) - 1)/2.
    #
    # Solving the inequality x_0 <= f_k(x) <= x_1, where 0 < x_0 < x_1 and 0 < k <= x yields:
    #
    #     - x_0/(k + 1) + k/2 <= x <= x_1/(k + 1) + k/2
    #         if k <= S(x_0) (or equivalently if T_k <= x_0)
    #
    #     - k <= x <= x_1/(k + 1) + k/2
    #         if S(x_0) < k < S(x_1) (or equivalently if x_0 <= T_k <= x_1) and k <= x.
    #
    # If k <= S(x_0), then it implies T_k <= x_0. Any valid x will have x_0 <= T_x, which implies
    # T_k <= T_x implies k <= x, and so the first situation applies.
    #
    # If k >= S(x_1), then any valid x will have x_1 >= T_x, which implies T_k >= T_x implies
    # k >= x, and so the net gain is T_x. Then the range of valid x will simply be:
    #
    #     - S(x_0) <= x <= S(x_1)
    #         if S(x_1) <= k
    #
    # The final situation, slightly trickier, is if S(x_0) < k < S(x_1). If k <= x then the second
    # situation from above applies, but if k > x, then similarly to above we must have S(x_0) <= x < k.
    # Thus, the set of valid x for the final situation is the union of [S(x_0), k) and [k, x_1/(k + 1) + k/2],
    # or in other words:
    #
    #     - S(x_0) <= x <= x_1/(k + 1) + k/2
    #         if S(x_0) < k < S(x_1).
    t_steps = triangular(steps)

    if t_steps <= x_0:
        lower = x_0/(steps + 1) + steps/2
        upper = x_1/(steps + 1) + steps/2
    elif t_steps >= x_1:
        lower = inverse_triangular(x_0)
        upper = inverse_triangular(x_1)
    else:
        lower = inverse_triangular(x_0)
        upper = x_1/(steps + 1) + steps/2

    return get_int_range(lower, upper)


@cli.command
@utils.part
def part_2_algebraic():
    x_0, x_1, y_0, y_1 = get_trench()

    solutions = set()
    # Note that we can bound steps above by -2 * y_0. For k > -2 * y_0, we can actually
    # see that get_valid_y will actually return an empty list. For even k, the interval
    # will be strictly contained in (k/2 - 1, k/2), and for odd k, the interval will be
    # strictly contained in ((k - 1)/2, (k - 1)/2 + 1).
    for steps in range(2 * -y_0):
        solutions.update(itertools.product(
            get_valid_x(steps, x_0, x_1),
            get_valid_y(steps, y_0, y_1),
        ))

    print(len(solutions))


if __name__ == '__main__':
    cli()
