import utils


def get_signal():
    return utils.get_input(__file__, cast=str, delimiter='', line_delimiter='\n')[0]


def get_marker_end(signal, size):
    for i in range(len(signal)):
        packet = signal[i:i + size]

        if len(set(packet)) == size:
            return i + size

    raise ValueError('No marker found')


@utils.part
def part_1():
    signal = get_signal()
    print(get_marker_end(signal, 4))


@utils.part
def part_2():
    signal = get_signal()
    print(get_marker_end(signal, 14))
