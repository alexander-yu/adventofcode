import itertools
import re

import utils


WRITE_REGEX = r'mem\[(?P<address>\d+)\]'


def set_bit(value, index, bit):
    if bit:
        return value | (1 << index)
    return value & ~(1 << index)


def resolve_floating_bits(initial_address, floating_bits):
    addresses = []
    bit_combinations = itertools.product([0, 1], repeat=len(floating_bits))

    for bits in bit_combinations:
        address = initial_address

        for i, bit in zip(floating_bits, bits):
            address = set_bit(address, i, bit)

        addresses.append(address)

    return addresses


class Mask:
    def __init__(self, bits, version):
        self.bits = dict(enumerate(reversed(bits)))
        self.version_handlers = {
            1: self._apply_v1,
            2: self._apply_v2,
        }
        if version not in self.version_handlers:
            raise ValueError(
                f'Expected version to be one of {[self.version_handlers.keys()]}, got: {version}'
            )
        self.version_handler = self.version_handlers[version]

    def _apply_v1(self, memory, address, value):
        for i, bit in self.bits.items():
            if bit != 'X':
                value = set_bit(value, i, int(bit))
            else:
                continue

        memory[address] = value

    def _apply_v2(self, memory, address, value):
        floating_bits = []

        for i, bit in self.bits.items():
            if bit == '1':
                address = set_bit(address, i, 1)
            elif bit == '0':
                continue
            else:
                floating_bits.append(i)

        if floating_bits:
            floating_addresses = resolve_floating_bits(address, floating_bits)
            for floating_address in floating_addresses:
                memory[floating_address] = value
        else:
            memory[address] = value

    def apply(self, memory, address, value):
        return self.version_handler(memory, address, value)


def run_program(version):
    instructions = utils.get_input(delimiter=' = ', cast=str)
    memory = {}
    mask = None

    for instruction, value in instructions:
        match = re.fullmatch(WRITE_REGEX, instruction)
        if match:
            address = int(match.group('address'))
            mask.apply(memory, address, int(value))
        else:
            mask = Mask(list(value), version)

    return memory


@utils.part
def part_1():
    memory = run_program(1)
    print(sum(memory.values()))


@utils.part
def part_2():
    memory = run_program(2)
    print(sum(memory.values()))
