import os
import pathlib
import sys


def _split_line(line, delimiter):
    return line.split(delimiter) if delimiter else list(line)


def get_input(test=False, delimiter=',', cast=int):
    path = pathlib.Path(sys.argv[0])
    problem_number = path.stem
    test_prefix = '_test' if test else ''
    input_file_name = f'{problem_number}{test_prefix}.txt'

    with open(os.path.join(path.parent, 'inputs', input_file_name), 'r') as f:
        lines = f.read().strip().split('\n')

    return [
        [cast(x) for x in _split_line(line, delimiter)]
        for line in lines
    ]
