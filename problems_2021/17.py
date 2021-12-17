import collections
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


@cli.command()
@utils.part(__name__, 1)
def part_1():
    *_, y_0, _ = get_trench()

    # Note that if y is the initial vertical velocity, and we assume trench is in 3rd quadrant,
    # meaning that we must have k > y, then the total gain will be
    # y + y - 1 + ... + 0 - 1 - ... - (k - y) = T_y - T_{k - y},
    # where k is the number of steps.  We also assume for this part that y > 0.
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


@cli.command()
@utils.part(__name__, 2)
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

            if y_0 <= t_i - t_j and t_i - t_j <= y_1:
                ys.add((i, i + j))
                ys.add((-i - 1, j - i - 1))

    # Create a mapping of step number k -> x values that can reach trench boundaries in k steps.
    # This does not properly account for the situation where if the probe has started falling vertically
    # within trench boundaries, we can add infinitely many steps (since the x value doesn't change).
    #
    # We also keep a set of step numbers where this scenario is possible.
    xs_by_k = collections.defaultdict(list)
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
            if x_0 <= t_i - t_j and t_i - t_j <= x_1:
                xs_by_k[i - j - 1].append(i)
                if j == 0:
                    verticals.add(i)

    # For each valid (y, k), find all valid x for that k. If k >= min(verticals), we encounter a scenario
    # where it could actually just be falling vertically. xs_by_k does not automatically track this,
    # so we need to manually check and add these scenarios.
    velocities = set()
    for y, k in ys:
        for x in xs_by_k[k]:
            velocities.add((x, y))
        if k >= min(verticals):
            for vertical in verticals:
                velocities.add((vertical, y))

    print(len(velocities))


if __name__ == '__main__':
    cli()
