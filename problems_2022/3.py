import string

from boltons import iterutils

import click

import utils


PRIORITIES = {
    letter: i + 1
    for i, letter in enumerate(
        string.ascii_lowercase + string.ascii_uppercase
    )
}


def get_data():
    return utils.get_input(__file__, cast=str, delimiter='', line_delimiter='\n')


def get_duplicate(sack):
    compartment_1 = set(sack[:len(sack)//2])
    compartment_2 = set(sack[len(sack)//2:])
    return (compartment_1 & compartment_2).pop()


def get_badge(sacks):
    return (set.intersection(*[set(sack) for sack in sacks])).pop()


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    data = get_data()

    print(sum(
        PRIORITIES[get_duplicate(sack)]
        for sack in data
    ))


@cli.command
@utils.part
def part_2():
    data = get_data()

    print(sum(
        PRIORITIES[get_badge(sacks)]
        for sacks in iterutils.chunked(data, 3)
    ))


if __name__ == '__main__':
    cli()
