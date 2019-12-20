import datetime
import os
import subprocess
import sys

import click

TEMPLATE = """
import click

import utils


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


def gen_file(path, content):
    if os.path.exists(path):
        raise Exception(f'File {path} already exists')

    with open(path, 'w') as f:
        f.write(content)

    # Open new files in vscode
    if sys.platform == 'win32':
        subprocess.call(['code.cmd', path])
    else:
        subprocess.call(['code', path])


@click.command()
@click.argument('problem', nargs=1)
@click.option('-y', '--year', type=int)
def cli(problem, year):
    year = year if year else datetime.datetime.now().year

    directory = os.path.join(os.getcwd(), f'problems_{year}')
    os.makedirs(directory, exist_ok=True)

    gen_file(os.path.join(directory, f'{problem}.py'), TEMPLATE.lstrip())

    input_directory = os.path.join(directory, 'inputs')
    os.makedirs(input_directory, exist_ok=True)

    gen_file(os.path.join(input_directory, f'{problem}.txt'), '')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
