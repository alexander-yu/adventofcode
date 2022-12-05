import ast
import dataclasses
import itertools
import math
import typing

import click

import utils


@dataclasses.dataclass
class Blast:
    left: typing.Optional[int] = None
    right: typing.Optional[int] = None


EMPTY = Blast()


@dataclasses.dataclass
class Node:
    value: typing.Optional[int] = None
    left: typing.Optional['Node'] = None
    right: typing.Optional['Node'] = None

    def is_leaf(self):
        return not self.left and not self.right

    def is_empty(self):
        return self.value is None and not self.left and not self.right

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return f'[{str(self.left)}, {str(self.right)}]'

    def __add__(self, other):
        if not isinstance(other, Node):
            raise ValueError(f'Cannot add Node with type {type(other).__name__}')

        if self.is_empty():
            return other.copy()

        result = Node(left=self.copy(), right=other.copy())
        while True:
            exploded, _ = result.explode()
            if not exploded:
                if not result.split():
                    break

        return result

    def __abs__(self):
        if self.is_leaf():
            return self.value

        return 3 * abs(self.left) + 2 * abs(self.right)

    @staticmethod
    def from_number(number):
        if isinstance(number, int):
            return Node(value=number)

        left, right = number
        return Node(
            left=Node.from_number(left),
            right=Node.from_number(right),
        )

    def add_value(self, value, side):
        current = self
        while not current.is_leaf():
            current = getattr(current, side)

        current.value += value

    def absorb_blast(self, blast, side, depth):
        if blast == EMPTY:
            return EMPTY

        if depth == 1:
            crater = Node(value=0)
            setattr(self, side, crater)

        other_side = 'right' if side == 'left' else 'left'
        blast_value = getattr(blast, other_side)

        if blast_value:
            getattr(self, other_side).add_value(blast_value, side)

        setattr(blast, other_side, None)
        return blast

    def explode(self, depth=4):
        if self.is_leaf():
            return False, EMPTY

        if depth == 0:
            return True, Blast(left=self.left.value, right=self.right.value)

        for side in ['left', 'right']:
            exploded, blast = getattr(self, side).explode(depth=depth - 1)
            if exploded:
                blast = self.absorb_blast(blast, side, depth)
                return True, blast

        return False, EMPTY

    def split_side(self, side):
        side_node = getattr(self, side)

        if side_node.is_leaf():
            if side_node.value >= 10:
                setattr(
                    self,
                    side,
                    Node.from_number(
                        [
                            math.floor(side_node.value / 2),
                            math.ceil(side_node.value / 2),
                        ],
                    ),
                )
                return True
            return False
        return side_node.split()

    def split(self):
        return self.split_side('left') or self.split_side('right')

    def copy(self):
        return Node(
            value=self.value,
            left=self.left.copy() if self.left else None,
            right=self.right.copy() if self.right else None,
        )


def get_numbers():
    return [
        Node.from_number(number)
        for number in utils.get_input(__file__, delimiter=None, cast=ast.literal_eval)
    ]


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    numbers = get_numbers()
    print(abs(sum(numbers, start=Node())))


@utils.part(cli)
def part_2():
    numbers = get_numbers()
    print(max(
        abs(number_1 + number_2)
        for number_1, number_2 in itertools.permutations(numbers, 2)
    ))
