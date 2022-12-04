import click

import utils


def get_data():
    return utils.get_input(__file__, cast=str, delimiter=',', line_delimiter='\n')


def get_sections(assignment):
    start, end = assignment.split('-')
    return set(range(int(start), int(end) + 1))


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    data = get_data()
    count = 0

    for assignment_1, assignment_2 in data:
        sections_1, sections_2 = get_sections(assignment_1), get_sections(assignment_2)

        if sections_1 <= sections_2 or sections_2 <= sections_1:
            count += 1

    print(count)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    data = get_data()
    count = 0

    for assignment_1, assignment_2 in data:
        sections_1, sections_2 = get_sections(assignment_1), get_sections(assignment_2)

        if sections_1 & sections_2:
            count += 1

    print(count)


if __name__ == '__main__':
    cli()
