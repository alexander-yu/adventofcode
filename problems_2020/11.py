import enum

import click

import utils


class PointType(enum.Enum):
    FLOOR = '.'
    EMPTY_SEAT = 'L'
    OCCUPIED_SEAT = '#'


class Grid(utils.Grid):
    def get_seats(self):
        seats = []
        for point, point_type in self.points.items():
            if point_type in [PointType.EMPTY_SEAT, PointType.OCCUPIED_SEAT]:
                seats.append(point)

        return seats

    def get_adjacent_occupied_seats(self, point):
        adjacent_occupied_seats = []
        row, col = point

        for i in [row - 1, row, row + 1]:
            for j in [col - 1, col, col + 1]:
                adjacent_point = (i, j)
                if adjacent_point != point and self.points.get(adjacent_point) == PointType.OCCUPIED_SEAT:
                    adjacent_occupied_seats.append(adjacent_point)

        return adjacent_occupied_seats

    def get_visible_occupied_seats(self, point):
        visible_occupied_seats = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                vector = (i, j)
                if vector != (0, 0):
                    visible_point = utils.add_vector(point, vector)

                    while self.points.get(visible_point) == PointType.FLOOR:
                        visible_point = utils.add_vector(visible_point, vector)

                    if self.points.get(visible_point) == PointType.OCCUPIED_SEAT:
                        visible_occupied_seats.append(visible_point)

        return visible_occupied_seats

    def get_occupied_seats(self):
        return [
            point
            for point, point_type in self.points.items()
            if point_type == PointType.OCCUPIED_SEAT
        ]


def apply_adjacency_rules(grid):
    changes = []
    new_grid = grid.clone()

    for seat in grid.get_seats():
        adjacent_occupied_seats = grid.get_adjacent_occupied_seats(seat)
        if grid[seat] == PointType.EMPTY_SEAT and not adjacent_occupied_seats:
            new_grid[seat] = PointType.OCCUPIED_SEAT
            changes.append(seat)
        elif grid[seat] == PointType.OCCUPIED_SEAT and len(adjacent_occupied_seats) >= 4:
            new_grid[seat] = PointType.EMPTY_SEAT
            changes.append(seat)

    return new_grid, changes


def apply_visibility_rules(grid):
    changes = []
    new_grid = grid.clone()

    for seat in grid.get_seats():
        visible_occupied_seats = grid.get_visible_occupied_seats(seat)
        if grid[seat] == PointType.EMPTY_SEAT and not visible_occupied_seats:
            new_grid[seat] = PointType.OCCUPIED_SEAT
            changes.append(seat)
        elif grid[seat] == PointType.OCCUPIED_SEAT and len(visible_occupied_seats) >= 5:
            new_grid[seat] = PointType.EMPTY_SEAT
            changes.append(seat)

    return new_grid, changes


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    grid = utils.get_grid(__file__, grid_cls=Grid, value_transformer=PointType, delimiter='', cast=str)
    while True:
        grid, changes = apply_adjacency_rules(grid)
        if not changes:
            print(len(grid.get_occupied_seats()))
            return


@cli.command
@utils.part
def part_2():
    grid = utils.get_grid(__file__, grid_cls=Grid, value_transformer=PointType, delimiter='', cast=str)
    while True:
        grid, changes = apply_visibility_rules(grid)
        if not changes:
            print(len(grid.get_occupied_seats()))
            return


if __name__ == '__main__':
    cli()
