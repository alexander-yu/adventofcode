import utils


def get_data():
    return utils.get_input(__file__, cast=int, delimiter='', line_delimiter='\n')


def is_visible(grid, i, j):
    height = grid[i][j]

    max_l = max(grid[i][:j], default=-1)
    max_r = max(grid[i][j + 1:], default=-1)
    max_u = max([grid[k][j] for k in range(i)], default=-1)
    max_d = max([grid[k][j] for k in range(i + 1, len(grid))], default=-1)

    return any(h < height for h in [max_l, max_r, max_u, max_d])


def visibility_score(grid, i, j):
    height = grid[i][j]
    score = 1

    for direction in utils.DIRECTIONS.values():
        direction = tuple(direction.flatten())
        distance = 0
        current = utils.add_vector((i, j), direction)

        while 0 <= current[0] < len(grid) and 0 <= current[1] < len(grid[0]):
            distance += 1

            if grid[current[0]][current[1]] >= height:
                break

            current = utils.add_vector(current, direction)

        score *= distance

    return score


@utils.part
def part_1():
    grid = get_data()

    count = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            count += is_visible(grid, i, j)

    print(count)


@utils.part
def part_2():
    grid = get_data()

    print(max(visibility_score(grid, i, j) for i in range(len(grid)) for j in range(len(grid[0]))))
