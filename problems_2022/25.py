import numpy as np

import utils


DIGITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}


def get_snafus():
    return utils.get_input(cast=str, delimiter=None, line_delimiter='\n')


def to_snafu(number):
    digits = []

    while number:
        carry = 0

        match residue := number % 5:
            case 0 | 1 | 2:
                digits.append(str(residue))
            case 3:
                digits.append('=')
                carry = 1
            case 4:
                digits.append('-')
                carry = 1

        number = number // 5 + carry

    return ''.join(reversed(digits))


def to_decimal(snafu):
    return sum(
        DIGITS[digit] * place
        for digit, place
        in zip(reversed(snafu), 5 ** np.arange(len(snafu)))
    )


@utils.part
def part_1():
    snafus = get_snafus()
    print(to_snafu(sum(to_decimal(snafu) for snafu in snafus)))
