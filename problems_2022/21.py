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


def get_data():
    rows = utils.get_input(cast=str, delimiter=': ', line_delimiter='\n')
    data = {}

    for monkey, job in rows:
        if job.isnumeric():
            data[monkey] = int(job)
        else:
            monkey_1, op, monkey_2 = job.split()
            data[monkey] = (OPS[op], monkey_1, monkey_2)

    return data


def evaluate(data, monkey):
    if not isinstance(data[monkey], tuple):
        return data[monkey]

    op, monkey_1, monkey_2 = data[monkey]
    return op(evaluate(data, monkey_1), evaluate(data, monkey_2))


@utils.part
def part_1():
    data = get_data()
    print(int(evaluate(data, 'root')))


@utils.part
def part_2():
    data = get_data()
    me = sympy.Symbol('humn')
    _, monkey_1, monkey_2 = data['root']

    data['humn'] = me
    data['root'] = (
        lambda monkey_1, monkey_2: sympy.solve(monkey_1 - monkey_2, me),
        monkey_1,
        monkey_2,
    )

    solutions = evaluate(data, 'root')
    print(int(utils.assert_one(solutions)))
