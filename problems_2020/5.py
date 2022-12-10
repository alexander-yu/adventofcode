import utils


UPPER_CHARS = ['B', 'R']


def seat_id(seating):
    bits = [str(int(char in UPPER_CHARS)) for char in seating]
    return int(''.join(bits), 2)


def get_seat_ids():
    seatings = utils.get_input(delimiter=None, cast=str)
    return [seat_id(seating) for seating in seatings]


@utils.part
def part_1():
    print(max(get_seat_ids()))


@utils.part
def part_2():
    seat_ids = get_seat_ids()

    min_seat_id = min(seat_ids)
    max_seat_id = max(seat_ids)
    missing_seat_id = set(range(min_seat_id, max_seat_id + 1)) - set(seat_ids)

    assert len(missing_seat_id) == 1

    print(missing_seat_id.pop())
