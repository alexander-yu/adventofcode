import datetime
import os
import subprocess

import click

TEMPLATE = """
import click


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    pass


@cli.command()
def part_2():
    pass


if __name__ == '__main__':
    cli()
"""


@click.command()
@click.argument('problem', nargs=1)
@click.option('-y', '--year', type=int)
def cli(problem, year):
    year = year if year else datetime.datetime.now().year

    directory = os.path.join(os.getcwd(), f'problems_{year}')
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, f'{problem}.py')
    if os.path.exists(path):
        raise Exception(f'File {path} already exists')

    with open(path, 'w') as f:
        f.write(TEMPLATE)

    # Open new file in vscode
    subprocess.call(['code.cmd', path])


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
