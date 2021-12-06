import collections

import click

import utils


def get_total_fish(days):
    timers = collections.Counter(utils.get_input(__file__)[0])

    for _ in range(days):
        birthing = timers[0]

        for i in range(8):
            timers[i] = timers[i + 1]

        timers[8] = birthing
        timers[6] += birthing

    return sum(timers.values())


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    print(get_total_fish(80))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    print(get_total_fish(256))


if __name__ == '__main__':
    cli()
