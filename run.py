import collections
import datetime
import importlib
import os
import re

import cachetools
import click

import utils


@cachetools.cached({})
def get_module(year, day):
    return importlib.import_module(f'problems_{year}.{day}')


def get_all_available_days(year):
    return [
        file.removesuffix('.py')
        for file in os.listdir(f'problems_{year}')
        if re.match(r'[0-9]+\.py', file)
    ]


def get_parts_by_day(year, problems):
    parts_by_day = collections.defaultdict(set)

    for problem in problems:
        if '.' in problem:
            day, part_id = problem.split('.', maxsplit=1)

            module = get_module(year, day)
            parts = utils.PART_REGISTRY[module.__name__]
            part = parts.get(part_id)

            if not part:
                raise click.ClickException(
                    f'Part {part_id} of {module} is not registered. Registered parts: {list(parts.keys())}'
                )

            parts_by_day[int(day)].add(part)
        else:
            day = problem
            module = get_module(year, day)
            parts_by_day[int(day)] = set(utils.PART_REGISTRY[module.__name__].values())

    return parts_by_day


def execute_day(context, parts):
    for part in sorted(parts, key=lambda part: part.id):
        print(f'--- PART {part.id} ---')
        context.invoke(part.cmd)
        print()


@click.command()
@click.argument('problems', nargs=-1)
@click.option('-y', '--year', nargs=1, type=int, default=datetime.datetime.now().year, show_default=True)
@click.option('-t', '--test', is_flag=True, default=False)
@click.option('-a', '--all', 'run_all', is_flag=True, default=False)
@click.pass_context
def cli(context, problems, year, test, run_all):
    utils.IS_TEST = test

    if run_all:
        if problems:
            raise click.ClickException('Cannot both specify problems and have -a/-all enabled')
        problems = get_all_available_days(year)

    parts_by_day = get_parts_by_day(year, problems)

    for day, parts in sorted(parts_by_day.items()):
        if len(parts_by_day) > 1:
            print(f'========== DAY {day} ==========\n')

        execute_day(context, parts)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
