import operator

import sympy
import z3

import utils


X = sympy.Symbol('x')

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def get_jobs():
    rows = utils.get_input(cast=str, delimiter=': ')
    jobs = {}

    for monkey, job in rows:
        if job.isnumeric():
            jobs[monkey] = int(job)
        else:
            monkey_1, op, monkey_2 = job.split()
            jobs[monkey] = (OPS[op], monkey_1, monkey_2)

    return jobs


def evaluate(jobs, monkey):
    if not isinstance(jobs[monkey], tuple):
        return jobs[monkey]

    op, monkey_1, monkey_2 = jobs[monkey]
    return op(evaluate(jobs, monkey_1), evaluate(jobs, monkey_2))


@utils.part
def part_1():
    jobs = get_jobs()
    print(int(evaluate(jobs, 'root')))


@utils.part
def part_2():
    jobs = get_jobs()
    me = sympy.Symbol('humn')
    _, monkey_1, monkey_2 = jobs['root']

    jobs['humn'] = me
    jobs['root'] = (
        lambda monkey_1, monkey_2: sympy.solve(monkey_1 - monkey_2, me),
        monkey_1,
        monkey_2,
    )

    solutions = evaluate(jobs, 'root')
    print(int(utils.assert_one(solutions)))


@utils.part
def part_2_z3():
    jobs = get_jobs()
    monkey_vars = {monkey: z3.Int(monkey) for monkey in jobs}
    solver = z3.Optimize()

    for monkey, job in jobs.items():
        if monkey == 'humn':
            continue

        monkey_var = monkey_vars[monkey]

        if isinstance(job, int):
            solver.add(monkey_var == job)
        else:
            op, monkey_1, monkey_2 = job
            monkey_1_var, monkey_2_var = monkey_vars[monkey_1], monkey_vars[monkey_2]

            if monkey == 'root':
                solver.add(monkey_1_var == monkey_2_var)
            else:
                solver.add(monkey_var == op(monkey_1_var, monkey_2_var))

    me = monkey_vars['humn']
    solver.minimize(me)
    assert solver.check() == z3.sat

    print(solver.model().eval(me).as_long())
