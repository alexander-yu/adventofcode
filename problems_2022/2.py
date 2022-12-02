import click

import utils


HANDS = {
    'A': 'R',
    'X': 'R',
    'B': 'P',
    'Y': 'P',
    'C': 'S',
    'Z': 'S',
}

VALUES = {
    'R': 1,
    'P': 2,
    'S': 3,
}

OUTCOMES = {
    ('R', 'R'): 3,
    ('S', 'S'): 3,
    ('P', 'P'): 3,
    ('R', 'P'): 6,
    ('R', 'S'): 0,
    ('P', 'S'): 6,
    ('P', 'R'): 0,
    ('S', 'R'): 6,
    ('S', 'P'): 0,
}

HAND_FROM_OUTCOME = {
    ('A', 'X'): 'S',
    ('B', 'X'): 'R',
    ('C', 'X'): 'P',
    ('A', 'Y'): 'R',
    ('B', 'Y'): 'P',
    ('C', 'Y'): 'S',
    ('A', 'Z'): 'P',
    ('B', 'Z'): 'S',
    ('C', 'Z'): 'R',
}


def score(a, b):
    a, b = HANDS[a], HANDS[b]
    return OUTCOMES[(a, b)] + VALUES[b]


def score_from_outcome(a, b):
    a, b = HANDS[a], HAND_FROM_OUTCOME[(a, b)]
    return OUTCOMES[(a, b)] + VALUES[b]


def get_data():
    return utils.get_input(__file__, cast=str, delimiter=' ', line_delimiter='\n')


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    data = get_data()
    print(sum(score(a, b) for a, b in data))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    data = get_data()
    print(sum(score_from_outcome(a, b) for a, b in data))


if __name__ == '__main__':
    cli()
