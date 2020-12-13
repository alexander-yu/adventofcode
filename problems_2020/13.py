import math

import click

import utils


def min_departure(min_timestamp, bus):
    return bus * math.ceil(min_timestamp / bus)


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    min_timestamp, buses = utils.get_input(__file__, delimiter=None, cast=str)
    min_timestamp = int(min_timestamp)
    buses = [int(bus) for bus in buses.split(',') if bus != 'x']

    departures = [min_departure(min_timestamp, bus) for bus in buses]
    bus, departure = min(zip(buses, departures), key=lambda x: x[1])

    print(bus * (departure - min_timestamp))


@cli.command()
def part_2():
    _, buses = utils.get_input(__file__, delimiter=None, cast=str)

    buses, offsets = zip(*[
        (int(bus), -1 * i)
        for i, bus in enumerate(buses.split(','))
        if bus != 'x'
    ])

    print(utils.chinese_remainder(offsets, buses))


if __name__ == '__main__':
    cli()
