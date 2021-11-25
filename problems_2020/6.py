import click

import utils


def get_group_answers():
    return utils.get_input(__file__, delimiter='\n', line_delimiter='\n\n', cast=str)


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    groups = get_group_answers()
    counts = sum(
        len(
            set.union(*[set(answers) for answers in group])
        )
        for group in groups
    )
    print(counts)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    groups = get_group_answers()
    counts = sum(
        len(
            set.intersection(*[set(answers) for answers in group])
        )
        for group in groups
    )
    print(counts)


if __name__ == '__main__':
    cli()
