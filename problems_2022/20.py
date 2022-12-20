import collections

import utils


def get_file():
    return utils.get_input(cast=int, delimiter=None, line_delimiter='\n')


class Number:
    def __init__(self, val):
        self.val = val


def mix(file, decrypt=False):
    key = 811589153 if decrypt else 1
    rounds = 10 if decrypt else 1

    numbers = collections.deque(Number(number * key) for number in file)
    ordering = list(numbers)

    for _ in range(rounds):
        for number in ordering:
            idx = numbers.index(number)
            numbers.rotate(-idx)
            numbers.popleft()
            numbers.rotate(-number.val)
            numbers.insert(0, number)

    return utils.CircularList(number.val for number in numbers)


def grove(file):
    zero = file.index(0)
    return [file[zero + offset] for offset in [1000, 2000, 3000]]


@utils.part
def part_1():
    file = get_file()
    file = mix(file)
    print(sum(grove(file)))


@utils.part
def part_2():
    file = get_file()
    file = mix(file, decrypt=True)
    print(sum(grove(file)))
