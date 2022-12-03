from boltons import iterutils

import click

import utils


def get_data():
    return utils.get_input(__file__, cast=str, delimiter='', line_delimiter='\n')


def get_duplicate(sack):
    compartment_1 = set(sack[:len(sack)//2])
    compartment_2 = set(sack[len(sack)//2:])
    return (compartment_1 & compartment_2).pop()


def priority(item):
    if item.islower():
        return ord(item) - 96
    return ord(item) - 38


def get_badge(sacks):
    return (set.intersection(*[set(sack) for sack in sacks])).pop()


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    data = get_data()

    print(sum(
        priority(get_duplicate(sack))
        for sack in data
    ))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    data = get_data()

    print(sum(
        priority(get_badge(sacks))
        for sacks in iterutils.chunked(data, 3)
    ))


if __name__ == '__main__':
    cli()
