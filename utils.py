import enum
import os
import pathlib
import sys

import numpy as np


def _split_line(line, delimiter):
    if delimiter == '':
        return list(line)
    elif delimiter is None:
        return [line]
    return line.split(delimiter)


def get_input(problem_file, test=False, delimiter=',', cast=int):
    problem_path = pathlib.Path(problem_file).resolve()
    problem_number = problem_path.stem
    test_prefix = '_test' if test else ''
    input_file_name = f'{problem_number}{test_prefix}.txt'

    with open(os.path.join(problem_path.parent, 'inputs', input_file_name), 'r') as f:
        lines = f.read().rstrip().split('\n')

    return [
        [cast(x) for x in _split_line(line, delimiter)]
        for line in lines
    ]


def add_vector(position, vector):
    return tuple(np.array(position) + vector)


class MultiValueEnum(enum.Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    def values(self):
        cls = type(self)
        return [value for value in cls._value2member_map_ if cls._value2member_map_[value] == self]
