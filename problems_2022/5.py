import utils


REAL_STACKS = [
    ['Q', 'W', 'P', 'S', 'Z', 'R', 'H', 'D'],
    ['V', 'B', 'R', 'W', 'Q', 'H', 'F'],
    ['C', 'V', 'S', 'H'],
    ['H', 'F', 'G'],
    ['P', 'G', 'J', ' B', 'Z'],
    ['Q', 'T', 'J', 'H', 'W', 'F', 'L'],
    ['Z', 'T', 'W', 'D', 'L', 'V', 'J', 'N'],
    ['D', 'T', 'Z', 'C', 'J', 'G', 'H', 'F'],
    ['W', 'P', 'V', 'M', 'B', 'H'],
]
TEST_STACKS = [
    ['Z', 'N'],
    ['M', 'C', 'D'],
    ['P'],
]

stacks = TEST_STACKS if utils.IS_TEST else REAL_STACKS


def get_data():
    return utils.get_input(__file__, cast=str, delimiter='\n', line_delimiter='\n\n')


def exec_move(move, stacks, crane=False):
    _, n, _, stack_1, _, stack_2 = move.split(' ')
    n = int(n)
    stack_1, stack_2 = int(stack_1), int(stack_2)

    if not crane:
        for _ in range(n):
            stacks[stack_2 - 1].append(stacks[stack_1 - 1].pop())
    else:
        crates = []
        for _ in range(n):
            crates.append(stacks[stack_1 - 1].pop())

        stacks[stack_2 - 1].extend(crates[::-1])


@utils.part
def part_1():
    _, moves = get_data()

    for move in moves:
        exec_move(move, stacks)

    print(''.join(stack[-1] for stack in stacks))


@utils.part
def part_2():
    _, moves = get_data()

    for move in moves:
        exec_move(move, stacks, crane=True)

    print(''.join(stack[-1] for stack in stacks))
