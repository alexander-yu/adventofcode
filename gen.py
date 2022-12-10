import datetime
import os
import subprocess
import sys

import click

PRE_PART_2 = """
import utils


def get_data():
    return utils.get_input(__file__, cast=int, delimiter=',', line_delimiter='\\n')


@utils.part
def part_1():
    data = get_data()
"""

PART_2 = """
@utils.part
def part_2():
    data = get_data()
"""


def gen_file(path, content, exists_ok=False):
    if os.path.exists(path):
        if exists_ok:
            return
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
        chunks = [PRE_PART_2]
    else:
        chunks = [PRE_PART_2, PART_2]

    return '\n\n'.join(chunk.lstrip() for chunk in chunks)


@click.command()
@click.argument('problem', nargs=1, type=int)
@click.option('-y', '--year', type=int, default=datetime.datetime.now().year, show_default=True)
def cli(problem, year):
    directory = os.path.join(os.getcwd(), f'problems_{year}')
    os.makedirs(directory, exist_ok=True)

    gen_file(os.path.join(directory, '__init__.py'), '', exists_ok=True)
    gen_file(os.path.join(directory, f'{problem}.py'), get_template(problem))

    input_directory = os.path.join(os.getcwd(), 'inputs', f'problems_{year}')
    os.makedirs(input_directory, exist_ok=True)

    gen_file(os.path.join(input_directory, f'{problem}.txt'), '')
    gen_file(os.path.join(input_directory, f'{problem}_test.txt'), '')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
