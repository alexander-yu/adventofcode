from boltons import iterutils
from cytoolz import itertoolz

import utils


def get_signal():
    return utils.get_input(cast=str, delimiter='', line_delimiter='\n')[0]


def get_marker_end(signal, size):
    for i in range(len(signal)):
        packet = signal[i:i + size]

        if len(set(packet)) == size:
            return i + size

    raise ValueError('No marker found')


def get_marker_end_boltons(signal, size):
    return iterutils.first(
        i + size
        for i, packet in enumerate(iterutils.windowed(signal, size))
        if not iterutils.redundant(packet)
    )


def get_marker_end_cytoolz(signal, size):
    return itertoolz.first(
        i + size
        for i, packet in enumerate(itertoolz.sliding_window(size, signal))
        if itertoolz.isdistinct(packet)
    )


@utils.part
def part_1():
    signal = get_signal()
    print(get_marker_end(signal, 4))


@utils.part
def part_2():
    signal = get_signal()
    print(get_marker_end(signal, 14))


@utils.part
def part_1_boltons():
    signal = get_signal()
    print(get_marker_end_boltons(signal, 4))


@utils.part
def part_2_boltons():
    signal = get_signal()
    print(get_marker_end_boltons(signal, 14))


@utils.part
def part_1_cytoolz():
    signal = get_signal()
    print(get_marker_end_cytoolz(signal, 4))


@utils.part
def part_2_cytoolz():
    signal = get_signal()
    print(get_marker_end_cytoolz(signal, 14))
