import collections

import utils


@utils.part
def part_1():
    adapters = sorted(utils.get_input(delimiter=None))
    inputs = [0] + adapters
    outputs = adapters + [max(adapters) + 3]
    differences = [output - input for output, input in zip(outputs, inputs)]
    counts = collections.Counter(differences)
    print(counts[1] * counts[3])


@utils.part
def part_2():
    adapters = sorted(utils.get_input(delimiter=None))

    combinations = collections.defaultdict(int, {0: 1})
    for adapter in adapters:
        combinations[adapter] = combinations[adapter - 1] + combinations[adapter - 2] + combinations[adapter - 3]

    print(combinations[adapters[-1]])
