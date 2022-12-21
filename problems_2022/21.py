import operator

import sympy

import utils


X = sympy.Symbol('x')

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def get_data(solve_for_x=False):
    rows = utils.get_input(cast=str, delimiter=': ', line_delimiter='\n')
    data = {}

    for monkey, job in rows:
        if solve_for_x and monkey == 'humn':
            data[monkey] = X
        elif job.isnumeric():
            data[monkey] = int(job)
        else:
            monkey_1, op, monkey_2 = job.split()
            data[monkey] = (OPS[op], monkey_1, monkey_2)

    return data


def evaluate(data, monkey, solve_for_x=False):
    if not isinstance(data[monkey], tuple):
        return data[monkey]

    op, monkey_1, monkey_2 = data[monkey]

    monkey_1, monkey_2 = evaluate(data, monkey_1), evaluate(data, monkey_2)

    if solve_for_x and monkey == 'root':
        return sympy.solve(monkey_1 - monkey_2, X)

    return op(monkey_1, monkey_2)


@utils.part
def part_1():
    data = get_data()
    print(int(evaluate(data, 'root')))


@utils.part
def part_2():
    data = get_data(solve_for_x=True)
    solutions = evaluate(data, 'root', solve_for_x=True)
    print(int(utils.assert_one(solutions)))
