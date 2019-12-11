import datetime
import importlib

import click


@click.command()
@click.argument('problem', nargs=1)
@click.argument('part', nargs=1, type=click.Choice(['part_1', 'part_2']))
@click.option('-y', '--year', type=int)
@click.pass_context
def cli(context, problem, part, year):
    year = year if year else datetime.datetime.now().year
    part_cmd = getattr(importlib.import_module(f'problems_{year}.{problem}'), part)
    context.invoke(part_cmd)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
