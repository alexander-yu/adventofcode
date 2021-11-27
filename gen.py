import datetime
import os
import subprocess
import sys

import click

PRE_PART_2 = """
import click

import utils


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    pass
"""

PART_2 = """
@cli.command()
@utils.part(__name__, 2)
def part_2():
    pass
"""

MAIN = """
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


def get_template(problem):
    if problem == 25:
        chunks = [PRE_PART_2, MAIN]
    else:
        chunks = [PRE_PART_2, PART_2, MAIN]

    return '\n\n'.join(chunk.lstrip() for chunk in chunks)


@click.command()
@click.argument('problem', nargs=1, type=int)
@click.option('-y', '--year', type=int, default=datetime.datetime.now().year, show_default=True)
def cli(problem, year):
    directory = os.path.join(os.getcwd(), f'problems_{year}')
    os.makedirs(directory, exist_ok=True)

    gen_file(os.path.join(directory, f'{problem}.py'), get_template(problem))

    input_directory = os.path.join(directory, 'inputs')
    os.makedirs(input_directory, exist_ok=True)

    gen_file(os.path.join(input_directory, f'{problem}.txt'), '')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
