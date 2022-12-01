import click

import utils


def get_calories_by_elf():
    calories_list = utils.get_input(__file__, delimiter='\n', line_delimiter='\n\n')
    return [sum(calories) for calories in calories_list]


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    calories = get_calories_by_elf()
    print(max(calories))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    calories = get_calories_by_elf()
    print(sum(sorted(calories, reverse=True)[:3]))


if __name__ == '__main__':
    cli()
