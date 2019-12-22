import functools
import itertools
import re

import click

from sympy.core import numbers

import utils


REVERSE_RE = r'deal into new stack'
CUT_RE = r'cut (-?\d+)'
INCREMENT_RE = r'deal with increment (\d+)'


@functools.lru_cache(maxsize=None)
def inverse(n, k):
    return numbers.mod_inverse(k, n)


def mod(n, *coeffs):
    return tuple(coeff % n for coeff in coeffs)


COEFFS = {
    REVERSE_RE: lambda n, a, b: mod(n, -1 * a, -1 * b - 1),
    CUT_RE: lambda n, k, a, b: mod(n, a, b - k),
    INCREMENT_RE: lambda n, k, a, b: mod(n, a * k, b * k),
}

INV_COEFFS = {
    REVERSE_RE: lambda n, a, b: mod(n, -1 * a, -1 * b - 1),
    CUT_RE: lambda n, k, a, b: mod(n, a, b + k),
    INCREMENT_RE: lambda n, k, a, b: mod(n, a * inverse(n, k), b * inverse(n, k)),
}


def get_coeffs(n, techniques, reverse=False):
    if reverse:
        techniques = techniques[::-1]
        coeff_map = INV_COEFFS
    else:
        coeff_map = COEFFS

    coeffs = (1, 0)
    for technique in techniques:
        for regex, method in coeff_map.items():
            match = re.match(regex, technique)
            if match:
                coeffs = method(*itertools.chain(
                    [n],
                    [int(arg) for arg in match.groups()],
                    coeffs,
                ))

    return coeffs


def shuffle(n, card, rounds=1, reverse=False):
    techniques = utils.get_input(__file__, delimiter=None, cast=str)
    a, b = get_coeffs(n, techniques, reverse=reverse)
    return (
        pow(a, rounds, n) * card +
        b * (pow(a, rounds, n) - 1) * inverse(n, a - 1)
    ) % n


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    print(shuffle(10007, 2019))

@cli.command()
def part_2():
    print(shuffle(119315717514047, 2020, rounds=101741582076661, reverse=True))


if __name__ == '__main__':
    cli()
