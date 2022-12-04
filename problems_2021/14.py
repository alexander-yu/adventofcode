import collections

import click

import utils


def apply_insertions(steps):
    polymer, rules = utils.get_input(__file__, delimiter=None, line_delimiter='\n\n', cast=str)
    rules = dict(utils.parse(rules, delimiter=' -> ', cast=str))

    pairs = collections.Counter(polymer[i:i + 2] for i in range(len(polymer) - 1))
    letters = collections.Counter(polymer)

    for _ in range(steps):
        old_pairs = pairs.copy()

        for rule, insertion in rules.items():
            left_pair = rule[0] + insertion
            right_pair = insertion + rule[1]
            count = old_pairs[rule]

            pairs[left_pair] += count
            pairs[right_pair] += count
            pairs[rule] -= count
            letters[insertion] += count

    return letters


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    letters = apply_insertions(10)
    most_common = letters.most_common()
    print(most_common[0][1] - most_common[-1][1])


@cli.command
@utils.part
def part_2():
    letters = apply_insertions(40)
    most_common = letters.most_common()
    print(most_common[0][1] - most_common[-1][1])


if __name__ == '__main__':
    cli()
