from collections import defaultdict

import utils


def is_nondecreasing(num):
    digits = [c for c in str(num)]

    for i in range(1, len(digits)):
        prev = digits[i - 1]
        curr = digits[i]

        if prev > curr:
            return False

    return True


def get_digit_adjacencies(num):
    adjacencies = defaultdict(lambda: 1)
    digits = [c for c in str(num)]

    for i in range(1, len(digits)):
        prev = digits[i - 1]
        curr = digits[i]

        if prev == curr:
            adjacencies[curr] += 1
        elif prev > curr:
            continue

    return adjacencies


@utils.part
def part_1():
    start, end = utils.get_input(delimiter='-')[0]

    print(len([
        num
        for num in range(start, end + 1)
        if is_nondecreasing(num) and len(get_digit_adjacencies(num)) > 0
    ]))


@utils.part
def part_2():
    start, end = utils.get_input(delimiter='-')[0]

    print(len([
        num
        for num in range(start, end + 1)
        if is_nondecreasing(num) and 2 in get_digit_adjacencies(num).values()
    ]))
