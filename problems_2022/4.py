import click

import utils


def get_data():
    return utils.get_input(__file__, cast=str, delimiter=',', line_delimiter='\n')


def get_sections(interval_pairs):
    for interval_1, interval_2 in interval_pairs:
        start_1, end_1 = interval_1.split('-')
        start_2, end_2 = interval_2.split('-')

        yield (
            set(range(int(start_1), int(end_1) + 1)),
            set(range(int(start_2), int(end_2) + 1)),
        )


def get_intervals(interval_pairs):
    for interval_1, interval_2 in interval_pairs:
        start_1, end_1 = interval_1.split('-')
        start_2, end_2 = interval_2.split('-')

        yield (
            [int(start_1), int(end_1)],
            [int(start_2), int(end_2)],
        )


@click.group()
def cli():
    pass


@cli.command()
@utils.part
def part_1():
    data = get_data()
    count = 0

    for sections_1, sections_2 in get_sections(data):
        if sections_1 <= sections_2 or sections_2 <= sections_1:
            count += 1

    print(count)


@cli.command()
@utils.part
def part_2():
    data = get_data()
    count = 0

    for sections_1, sections_2 in get_sections(data):
        if sections_1 & sections_2:
            count += 1

    print(count)


@cli.command()
@utils.part
def part_1_interval():
    data = get_data()
    count = 0

    for (start_1, end_1), (start_2, end_2) in get_intervals(data):
        if start_1 <= start_2 <= end_2 <= end_1 or start_2 <= start_1 <= end_1 <= end_2:
            count += 1

    print(count)


@cli.command()
@utils.part
def part_2_interval():
    data = get_data()
    count = 0

    for (start_1, end_1), (start_2, end_2) in get_intervals(data):
        if not (end_1 < start_2 or end_2 < start_1):
            count += 1

    print(count)


if __name__ == '__main__':
    cli()
