from typing import Callable

import dataclasses
import math

import parse

import utils


@dataclasses.dataclass
class Monkey:
    items: list
    operation: Callable
    mod: int
    test_true: int
    test_false: int
    inspect_count: int = 0

    @staticmethod
    def parse(lines):
        items = [
            int(item) for item in parse.parse(
                'Starting items: {}', lines[1]
            )[0].split(', ')
        ]
        operation_expr = parse.parse('Operation: new = {}', lines[2])[0]
        operation = eval(f'lambda old: {operation_expr}')
        mod = parse.parse('Test: divisible by {:d}', lines[3])[0]
        test_true = parse.parse('If true: throw to monkey {:d}', lines[4])[0]
        test_false = parse.parse('If false: throw to monkey {:d}', lines[5])[0]
        return Monkey(items, operation, mod, test_true, test_false)


def get_monkeys():
    data = utils.get_input(cast=lambda line: line.lstrip(' '), delimiter='\n', line_delimiter='\n\n')
    return [Monkey.parse(lines) for lines in data]


def get_monkey_business(num_rounds, relief=True):
    monkeys = get_monkeys()
    mod_lcm = math.lcm(*[monkey.mod for monkey in monkeys])

    for _ in range(num_rounds):
        for monkey in monkeys:
            for item in monkey.items:
                worry = monkey.operation(item)

                if relief:
                    worry //= 3
                else:
                    worry %= mod_lcm

                if worry % monkey.mod == 0:
                    monkeys[monkey.test_true].items.append(worry)
                else:
                    monkeys[monkey.test_false].items.append(worry)

                monkey.inspect_count += 1
                monkey.items = []

    top_monkeys = sorted(monkeys, key=lambda monkey: monkey.inspect_count, reverse=True)
    return top_monkeys[0].inspect_count * top_monkeys[1].inspect_count


@utils.part
def part_1():
    print(get_monkey_business(20))


@utils.part
def part_2():
    print(get_monkey_business(10000, relief=False))
