import dataclasses
import itertools
import typing

import click
import numpy as np

import utils


@dataclasses.dataclass(frozen=True)
class Scanner:
    id: int
    points: typing.FrozenSet[tuple]

    def __iter__(self):
        return iter(self.points)


def rotated_match(scanner_1, scanner_2):
    for point_1, point_2 in itertools.product(scanner_1, scanner_2):
        diff = tuple(x - y for x, y in zip(point_1, point_2))
        oriented_scanner_2 = Scanner(
            scanner_2.id,
            frozenset([utils.add_vector(point, diff) for point in scanner_2]),
        )
        if len(scanner_1.points & oriented_scanner_2.points) >= 12:
            return oriented_scanner_2, diff

    return None


def match(scanner_1, scanner_2):
    for rotation in utils.ROTATIONS_3D:
        rotated_scanner_2 = Scanner(
            scanner_2.id,
            frozenset(tuple(np.dot(rotation, point)) for point in scanner_2),
        )
        result = rotated_match(scanner_1, rotated_scanner_2)
        if result:
            return result

    return None


def orient_one(oriented, unlocated, positions, cache):
    for scanner_2 in unlocated:
        for scanner_1 in oriented:
            if (scanner_2.id, scanner_1.id) in cache:
                continue

            print(f'Matching {scanner_2.id} to {scanner_1.id}')
            result = match(scanner_1, scanner_2)
            if result:
                oriented_scanner_2, position = result
                print(f'MATCH: {position}')

                oriented.append(oriented_scanner_2)
                positions.append(position)
                unlocated.remove(scanner_2)
                return
            cache.add((scanner_2.id, scanner_1.id))

    raise ValueError('Could not orient a scanner')


def orient(scanners):
    oriented, unlocated = scanners[:1], set(scanners[1:])
    positions = [(0, 0, 0)]
    cache = set()

    while unlocated:
        orient_one(oriented, unlocated, positions, cache)

    return oriented, positions


def get_scanners():
    scanner_entries = utils.get_input(__file__, delimiter=None, line_delimiter='\n\n', cast=str)
    scanners = []
    for i, scanner_entry in enumerate(scanner_entries):
        coordinates = utils.parse(scanner_entry, delimiter=None, cast=str)[1:]
        scanners.append(Scanner(
            i,
            frozenset(
                tuple(utils.parse(coordinate)[0])
                for coordinate in coordinates
            )
        ))

    return scanners


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    scanners = get_scanners()
    oriented, _ = orient(scanners)
    print(len(set(itertools.chain.from_iterable(oriented))))


@cli.command
@utils.part
def part_2():
    scanners = get_scanners()
    _, positions = orient(scanners)
    print(max(
        sum(abs(x - y) for x, y in zip(position_1, position_2))
        for position_1, position_2 in itertools.combinations(positions)
    ))


if __name__ == '__main__':
    cli()
