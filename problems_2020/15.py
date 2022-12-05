import collections

import click

import utils


def play(last_round):
    numbers = utils.get_input(__file__)[0]

    occurrences = collections.defaultdict(list, {number: [i] for i, number in enumerate(numbers)})
    last_number = numbers[-1]

    i = len(numbers)

    while i < last_round:
        if len(occurrences[last_number]) == 1:
            last_number = 0
        else:
            last_two_occurrences = occurrences[last_number][-2:]
            last_number = last_two_occurrences[1] - last_two_occurrences[0]

        occurrences[last_number].append(i)
        i += 1

    print(last_number)


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    play(2020)


@utils.part(cli)
def part_2():
    play(30000000)
