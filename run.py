import datetime
import importlib

import click

import utils


@click.command()
@click.argument('problem', nargs=1)
@click.option('-p', 'part', nargs=1)
@click.option('-y', '--year', nargs=1, type=int, default=datetime.datetime.now().year, show_default=True)
@click.option('-t/-r', '--test/--real', default=False, show_default=True)
@click.pass_context
def cli(context, problem, part, year, test):
    if '.' in problem:
        problem, part_id = problem.split('.', maxsplit=1)
        if part_id and part:
            raise ValueError(f'Part is defined twice, once as {part_id} and once as {part}')

        part = part_id or part

    module = importlib.import_module(f'problems_{year}.{problem}')
    parts = utils.PART_REGISTRY[module.__name__]
    utils.IS_TEST = test

    if part:
        part_cmd = parts.get(part)

        if not part_cmd:
            raise ValueError(
                f'Part {part} of {module} is not registered. Registered parts: {list(parts.keys())}'
            )

        context.invoke(part_cmd)
        print()
    else:
        for part_id, part_cmd in sorted(parts.items()):
            print(f'=== PART {part_id} ===')
            context.invoke(part_cmd)
            print()


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
