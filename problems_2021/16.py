import dataclasses
import enum
import math

import click

import utils


class PacketType(enum.Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7


@dataclasses.dataclass
class Header:
    version_id: int
    type: PacketType


class Packet:
    EVAL_HANDLERS = {
        PacketType.SUM: sum,
        PacketType.PRODUCT: math.prod,
        PacketType.MIN: min,
        PacketType.MAX: max,
        PacketType.GT: lambda args: args[0] > args[1],
        PacketType.LT: lambda args: args[0] < args[1],
        PacketType.EQ: lambda args: args[0] == args[1],
    }

    def __init__(self, header, value=None, subpackets=None):
        self.header = header
        self.value = value
        self.subpackets = subpackets or []

    def version_sum(self):
        return self.header.version_id + sum(subpacket.version_sum() for subpacket in self.subpackets)

    def eval(self):
        if self.header.type == PacketType.LITERAL:
            return self.value

        return self.EVAL_HANDLERS[self.header.type]([
            subpacket.eval() for subpacket in self.subpackets
        ])


def shift(data, num_bits, binary=False):
    bits = data[:num_bits]
    return bits if binary else int(bits, 2), data[num_bits:]


def parse_header(data):
    version_id, data = shift(data, 3)
    type_id, data = shift(data, 3)
    return Header(version_id, PacketType(type_id)), data


def parse_literal(data):
    value = 0
    group_bit, data = shift(data, 1)

    while group_bit == 1:
        group, data = shift(data, 4)
        value = 16 * value + group
        group_bit, data = shift(data, 1)

    group, data = shift(data, 4)
    value = 16 * value + group
    return value, data


def parse_subpackets_by_length(data):
    total_length, data = shift(data, 15)
    subpacket_data, data = shift(data, total_length, binary=True)
    subpackets = []

    while subpacket_data:
        subpacket, subpacket_data = parse_packet(subpacket_data)
        subpackets.append(subpacket)

    return subpackets, data


def parse_subpackets_by_count(data):
    total_subpackets, data = shift(data, 11)
    subpackets = []

    for _ in range(total_subpackets):
        subpacket, data = parse_packet(data)
        subpackets.append(subpacket)

    return subpackets, data


def parse_packet(data):
    header, data = parse_header(data)

    if header.type == PacketType.LITERAL:
        value, data = parse_literal(data)
        return Packet(header, value=value), data

    length_type_id, data = shift(data, 1)

    if length_type_id == 0:
        subpackets, data = parse_subpackets_by_length(data)
    else:
        subpackets, data = parse_subpackets_by_count(data)

    return Packet(header, subpackets=subpackets), data


def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)


def parse_transmission():
    transmission = hex_to_bin(utils.get_input(__file__, delimiter=None, cast=str)[0])
    packet, _ = parse_packet(transmission)
    return packet


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    transmission = parse_transmission()
    print(transmission.version_sum())


@utils.part(cli)
def part_2():
    transmission = parse_transmission()
    print(transmission.eval())


if __name__ == '__main__':
    cli()
