import datetime
import importlib

import click

import utils


@click.command()
@click.argument('problem', nargs=1)
@click.argument('part', nargs=1, type=int)
@click.option('-y', '--year', type=int)
@click.pass_context
def cli(context, problem, part, year):
    year = year if year else datetime.datetime.now().year
    module = importlib.import_module(f'problems_{year}.{problem}')
    parts = utils.PART_REGISTRY[module.__name__]
    part_cmd = parts.get(part)

    if not part_cmd:
        raise ValueError(
            f'Part {part} of {module} is not registered. Registered parts: {list(parts.keys())}'
        )

    context.invoke(part_cmd)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
