import collections

import click

import utils


def get_rating(numbers, zero_bit_criteria):
    index = 0
    numbers = numbers[:]

    while len(numbers) != 1:
        count = collections.Counter(number[index] for number in numbers)

        if count['0'] > count['1']:
            bit = str(zero_bit_criteria)
        else:
            bit = str(1 - zero_bit_criteria)

        numbers = [num for num in numbers if num[index] == bit]
        index += 1

    return int(numbers[0], 2)


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    numbers = utils.get_input(__file__, delimiter=None, cast=str)
    bit_length = len(numbers[0])

    gamma = [
        collections.Counter(
            number[i] for number in numbers
        ).most_common(1)[0][0]
        for i in range(bit_length)
    ]
    gamma = int(''.join(gamma), 2)
    epsilon = ((1 << bit_length) - 1) ^ gamma

    print(gamma * epsilon)


@cli.command
@utils.part
def part_2():
    numbers = utils.get_input(__file__, delimiter=None, cast=str)
    oxygen = get_rating(numbers, 0)
    co2 = get_rating(numbers, 1)
    print(oxygen * co2)


if __name__ == '__main__':
    cli()
