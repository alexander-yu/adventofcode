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


def score(opponent, me):
    return OUTCOMES[(opponent, me)] + VALUES[me]


def get_data():
    return utils.get_input(cast=str, delimiter=' ')


@utils.part
def part_1():
    data = get_data()
    print(sum(
        score(HANDS[opponent], HANDS[me])
        for opponent, me in data
    ))


@utils.part
def part_2():
    data = get_data()
    print(sum(
        score(HANDS[opponent], HAND_FROM_OUTCOME[(opponent, me)])
        for opponent, me in data
    ))
