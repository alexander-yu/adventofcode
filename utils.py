import enum
import os
import pathlib

import numpy as np


def _split_line(line, delimiter, cast):
    if delimiter == '':
        return list(cast(ch) for ch in line)
    elif delimiter is None:
        return cast(line)
    return [cast(item) for item in line.split(delimiter)]


def get_input(problem_file, test=False, delimiter=',', cast=int):
    problem_path = pathlib.Path(problem_file).resolve()
    problem_number = problem_path.stem
    test_prefix = '_test' if test else ''
    input_file_name = f'{problem_number}{test_prefix}.txt'

    with open(os.path.join(problem_path.parent, 'inputs', input_file_name), 'r') as f:
        lines = f.read().rstrip().split('\n')

    return [
        _split_line(line, delimiter, cast)
        for line in lines
    ]


def add_vector(position, vector):
    return tuple(np.array(position) + np.array(vector))


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
