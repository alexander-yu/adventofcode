import datetime
import importlib

import click

import utils


@click.command()
@click.argument('problem', nargs=1)
@click.option('-p', 'part', nargs=1, type=int)
@click.option('-y', '--year', nargs=1, type=int, default=datetime.datetime.now().year, show_default=True)
@click.pass_context
def cli(context, problem, part, year):
    module = importlib.import_module(f'problems_{year}.{problem}')
    parts = utils.PART_REGISTRY[module.__name__]

    if part:
        part_cmd = parts.get(part)

        if not part_cmd:
            raise ValueError(
                f'Part {part} of {module} is not registered. Registered parts: {list(parts.keys())}'
            )

        context.invoke(part_cmd)
        print()
    else:
        for i, (part, part_cmd) in enumerate(sorted(parts.items())):
            print(f'=== PART {part} ===')
            context.invoke(part_cmd)
            print()


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
