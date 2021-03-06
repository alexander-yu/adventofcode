import collections

import click

import utils


class PocketDimension:
    def __init__(self, active_points):
        self.active_points = set(active_points)

    def _run_cycle(self):
        new_active_points = set()
        active_neighbor_count = collections.defaultdict(int)

        for point in self.active_points:
            for neighbor in utils.get_neighbors(point):
                active_neighbor_count[neighbor] += 1

        for point, active_neighbors in active_neighbor_count.items():
            if point in self.active_points and active_neighbors in [2, 3]:
                new_active_points.add(point)
            elif point not in self.active_points and active_neighbors == 3:
                new_active_points.add(point)

        self.active_points = new_active_points

    def boot_up(self):
        for _ in range(6):
            self._run_cycle()


def get_pocket_dimension(dims):
    points = utils.get_input(__file__, delimiter='', cast=str)
    active_points = set()

    for i, row in enumerate(points):
        for j, status in enumerate(row):
            if status == '#':
                point = (i, j) + tuple(0 for _ in range(dims - 2))
                active_points.add(point)

    return PocketDimension(active_points)


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    pocket_dimension = get_pocket_dimension(3)
    pocket_dimension.boot_up()
    print(len(pocket_dimension.active_points))


@cli.command()
def part_2():
    pocket_dimension = get_pocket_dimension(4)
    pocket_dimension.boot_up()
    print(len(pocket_dimension.active_points))


if __name__ == '__main__':
    cli()
