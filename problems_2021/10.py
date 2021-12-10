import enum
import itertools
import statistics

import click

import utils


PAIRS = [
    '<>',
    '()',
    '[]',
    '{}',
]
OPENERS = set(pair[0] for pair in PAIRS)
CLOSERS = set(pair[1] for pair in PAIRS)
OPPOSITES = dict(itertools.chain.from_iterable(
    [(pair[0], pair[1]), (pair[1], pair[0])]
    for pair in PAIRS
))


class Status(enum.Enum):
    INCOMPLETE = 'INCOMPLETE'
    CORRUPTED = 'CORRUPTED'


def evaluate(line):
    stack = []

    for character in line:
        if character in OPENERS:
            stack.append(character)
        else:
            assert character in CLOSERS
            if stack[-1] == OPPOSITES[character]:
                stack.pop()
            else:
                return character, Status.CORRUPTED

    assert len(stack) > 0

    completion = []

    while stack:
        assert stack[-1] in OPENERS
        character = stack.pop()
        completion.append(OPPOSITES[character])

    return completion, Status.INCOMPLETE


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    lines = utils.get_input(__file__, test=False, delimiter='', cast=str)
    score_map = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    score = 0

    for line in lines:
        character, status = evaluate(line)
        if status == Status.CORRUPTED:
            score += score_map[character]

    print(score)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    lines = utils.get_input(__file__, test=False, delimiter='', cast=str)
    score_map = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    scores = []

    for line in lines:
        completion, status = evaluate(line)
        if status == Status.INCOMPLETE:
            score = 0

            for character in completion:
                score *= 5
                score += score_map[character]

            scores.append(score)

    print(statistics.median(scores))


if __name__ == '__main__':
    cli()
