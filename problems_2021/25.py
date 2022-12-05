import click

import utils


def move_herd(grid, herd, new_point_func):
    points = [point for point, value in grid.items() if value == herd]
    moves = []

    for point in points:
        new_point = new_point_func(point)
        if grid[new_point] == '.':
            moves.append((point, new_point))

    for point, new_point in moves:
        grid[point] = '.'
        grid[new_point] = herd

    return len(moves)


def move_east(grid):
    return move_herd(
        grid,
        '>',
        lambda point: (point[0], (point[1] + 1) % grid.columns),
    )


def move_south(grid):
    return move_herd(
        grid,
        'v',
        lambda point: ((point[0] + 1) % grid.rows, point[1]),
    )


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    grid = utils.get_grid(__file__, delimiter='', cast=str)
    step = 0

    while True:
        moves = move_east(grid)
        moves += move_south(grid)
        step += 1

        if not moves:
            print(step)
            break
