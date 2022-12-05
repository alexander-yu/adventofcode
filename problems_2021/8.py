import utils


def solve(digits, output):
    one = utils.assert_one(digits, lambda digit: len(digit) == 2)
    seven = utils.assert_one(digits, lambda digit: len(digit) == 3)
    four = utils.assert_one(digits, lambda digit: len(digit) == 4)
    eight = utils.assert_one(digits, lambda digit: len(digit) == 7)
    nine = utils.assert_one(digits, lambda digit: len(digit) == 6 and four <= digit)
    two = utils.assert_one(digits, lambda digit: len(digit) == 5 and len(nine - digit) == 2)
    three = utils.assert_one(digits, lambda digit: len(digit) == 5 and len(two - digit) == 1)
    five = utils.assert_one(digits, lambda digit: len(digit) == 5 and digit not in {two, three})
    zero = utils.assert_one(digits, lambda digit: len(digit) == 6 and digit != nine and one <= digit)
    six = utils.assert_one(digits, lambda digit: len(digit) == 6 and digit not in {zero, nine})

    mapping = {
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
        zero: '0',
    }
    return int(''.join(
        mapping[digit]
        for digit in output
    ))


@utils.part
def part_1():
    entries = utils.get_input(__file__, delimiter=' | ', cast=str)

    print(len([
        digit
        for _, output in entries
        for digit in output.split()
        if len(digit) in {2, 3, 4, 7}
    ]))


@utils.part
def part_2():
    entries = utils.get_input(__file__, delimiter=' | ', cast=str)
    result = 0

    for digits, output in entries:
        digits = [frozenset(digit) for digit in digits.split()]
        output = [frozenset(digit) for digit in output.split()]
        result += solve(digits, output)

    print(result)
