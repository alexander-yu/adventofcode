import utils


def run_step(grid):
    flashed = set()

    for point in grid:
        grid[point] += 1

    flashing = set(point for point, value in grid.items() if value > 9)

    while flashing:
        point = flashing.pop()

        for neighbor in grid.neighbors(point):
            grid[neighbor] += 1
            if grid[neighbor] > 9 and neighbor not in flashed:
                flashing.add(neighbor)

        flashed.add(point)

    for point in flashed:
        grid[point] = 0

    return flashed


@utils.part
def part_1():
    grid = utils.get_grid(__file__, grid_cls=utils.DiagonalGrid, delimiter='')
    flash_count = 0

    for _ in range(100):
        flashed = run_step(grid)
        flash_count += len(flashed)

    print(flash_count)


@utils.part
def part_2():
    grid = utils.get_grid(__file__, grid_cls=utils.DiagonalGrid, delimiter='')
    step = 0

    while True:
        step += 1
        flashed = run_step(grid)

        if len(flashed) == len(grid):
            print(step)
            break
