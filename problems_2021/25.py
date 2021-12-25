import click

import utils


def move_east(grid):
    points = [point for point, value in grid.items() if value == '>']
    moves = []

    for point in points:
        new_point = (point[0], (point[1] + 1) % grid.columns)
        if grid[new_point] == '.':
            moves.append((point, new_point))

    for point, new_point in moves:
        grid[point] = '.'
        grid[new_point] = '>'

    return len(moves)


def move_south(grid):
    points = [point for point, value in grid.items() if value == 'v']
    moves = []

    for point in points:
        new_point = ((point[0] + 1) % grid.rows, point[1])
        if grid[new_point] == '.':
            moves.append((point, new_point))

    for point, new_point in moves:
        grid[point] = '.'
        grid[new_point] = 'v'

    return len(moves)


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
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


if __name__ == '__main__':
    cli()
