import itertools

import click

import utils


def get_expenses():
    return set(itertools.chain.from_iterable(utils.get_input(__file__, delimiter=None)))


def get_expense_sum_pair(expenses, total):
    for expense in expenses:
        if (total - expense) in expenses:
            return expense, total - expense

    raise ValueError(f'Could not find two entries that sum to {total}')


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    expenses = get_expenses()
    expense_1, expense_2 = get_expense_sum_pair(expenses, 2020)
    print(expense_1 * expense_2)


@cli.command()
def part_2():
    expenses = get_expenses()
    for expense_1 in expenses:
        try:
            expense_2, expense_3 = get_expense_sum_pair(expenses, 2020 - expense_1)
            print(expense_1 * expense_2 * expense_3)
            return
        except ValueError:
            continue

    raise ValueError('Could not find three entries that sum to 2020')


if __name__ == '__main__':
    cli()
