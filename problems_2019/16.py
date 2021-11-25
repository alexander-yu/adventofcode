import click
import numpy as np

import utils

# TODO: fix for offsets
def interpolate(signal, offset=0):
    cum_sums = np.cumsum(signal)
    new_signal = []

    for i in range(offset, len(signal) + offset):
        digit = 0

        for j in range(i, len(signal) + offset, 4 * i + 4):
            j -= offset
            upper = cum_sums[min(j + i, len(signal) - 1)]
            lower = cum_sums[j - 1] if j else 0
            digit += upper - lower

        for j in range(3 * i + 2, len(signal) + offset, 4 * i + 4):
            j -= offset
            upper = cum_sums[min(j + i, len(signal) - 1)]
            lower = cum_sums[j - 1] if j else 0
            digit -= upper - lower

        digit = abs(digit) % 10
        new_signal.append(digit)

    return new_signal


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    signal = utils.get_input(__file__, delimiter='', cast=int)[0]

    for _ in range(100):
        signal = interpolate(signal)

    print(''.join(str(digit) for digit in signal))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    signal = utils.get_input(__file__, delimiter=None, cast=str)[0]
    signal *= 10000
    offset = int(signal[:7])
    signal = [int(c) for c in signal]
    signal = signal[offset:]

    for i in range(100):
        # The offset is > half of the entire signal, meaning that we just need to
        # generate cumulative sums for the digits, since for offset > n / 2, every
        # digit's pattern is either 0 if it's below the offset and 1 if it's at or greater
        # than the offset. In particular, this solution is super quick but relies on the
        # fact that the actual input for the problem has a very high offset.
        #
        # The more generalizable approach using interpolate() (which is O(n log n))
        # requires only computing the slice sums for ranges that are multiplied by 1 or -1.
        # At each offset the computations required are N, N/2, N/3, etc. leading to a total
        # O(n log n) complexity for each phase.
        signal = (np.cumsum(signal[::-1]) % 10)[::-1]
        #signal = interpolate(signal, offset=offset)
        print(i)

    print(''.join(str(digit) for digit in signal[:8]))


if __name__ == '__main__':
    cli()
