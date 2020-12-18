import click

import utils


def parse_expression(expression):
    tokens = []

    for char in expression:
        if char.isnumeric():
            digit = int(char)
            if tokens:
                top = tokens[-1]
                if isinstance(top, int):
                    tokens[-1] = 10 * top + digit
                else:
                    tokens.append(digit)
            else:
                tokens.append(digit)
        elif char in '+*()':
            tokens.append(char)

    return tokens


def reduce_expression(args, ops):
    op = ops.pop()
    arg_1, arg_2 = args.pop(), args.pop()
    if op == '+':
        args.append(arg_1 + arg_2)
    elif op == '*':
        args.append(arg_1 * arg_2)
    else:
        raise ValueError(f'Invalid op {op}')


def previous_has_precedence(previous_op, op, advanced):
    if advanced:
        if previous_op == '+':
            return True
        if op == '+':
            return False
        return True
    return True


def eval_expression(expression, advanced=False):
    tokens = parse_expression(expression)
    args = []
    ops = []

    for token in tokens:
        if isinstance(token, int):
            args.append(token)
        elif token == '(':
            ops.append(token)
        elif token in '+*':
            while ops and ops[-1] != '(' and previous_has_precedence(ops[-1], token, advanced):
                reduce_expression(args, ops)

            ops.append(token)
        else:
            while ops[-1] != '(':
                reduce_expression(args, ops)

            ops.pop()

    while ops:
        reduce_expression(args, ops)

    assert len(args) == 1
    return args[0]


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    expressions = utils.get_input(__file__, delimiter='', cast=str)
    print(sum([eval_expression(expression) for expression in expressions]))


@cli.command()
def part_2():
    expressions = utils.get_input(__file__, delimiter='', cast=str)
    print(sum([eval_expression(expression, advanced=True) for expression in expressions]))


if __name__ == '__main__':
    cli()
