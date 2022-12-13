import collections
import string

import networkx as nx

import utils


HEIGHTS = {
    letter: index
    for index, letter
    in enumerate(string.ascii_lowercase)
} | {'S': 0, 'E': 25}


class ElevationGrid(utils.Grid):
    def to_graph(self):
        graph = nx.DiGraph()
        for point, value in self.points.items():
            graph.add_node(point, value=value, height=HEIGHTS[value])

        for point in self.points:
            if self.points[point] == 'S':
                self.start = point
            elif self.points[point] == 'E':
                self.end = point

            for neighbor in point.neighbors():
                if neighbor in self.points:
                    if graph.nodes[neighbor]['height'] <= graph.nodes[point]['height'] + 1:
                        graph.add_edge(point, neighbor)

        return graph


@utils.part
def part_1():
    grid = utils.get_grid(grid_cls=ElevationGrid, cast=str, delimiter='')
    print(nx.shortest_path_length(grid.graph, grid.start, grid.end))


@utils.part
def part_2():
    grid = utils.get_grid(grid_cls=ElevationGrid, cast=str, delimiter='')
    print(min(
        length
        for point, length in nx.single_target_shortest_path_length(grid.graph, grid.end)
        if grid.graph.nodes[point]['height'] == 0
    ))


def shortest_path_to_end(grid, sources):
    end, _ = utils.assert_one(grid.items(), key=lambda item: item[1] == 'E')
    seen = set(sources)
    queue = collections.deque([(point, 0) for point in seen])

    while queue:
        point, distance = queue.popleft()
        if point == end:
            return distance

        for neighbor in point.neighbors():
            if (
                neighbor in grid and
                neighbor not in seen and
                HEIGHTS[grid[neighbor]] <= HEIGHTS[grid[point]] + 1
            ):
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))


@utils.part
def part_1_bfs():
    grid = utils.get_grid(cast=str, delimiter='', parse_graph=False)
    start, _ = utils.assert_one(grid.items(), key=lambda item: item[1] == 'S')
    print(shortest_path_to_end(grid, [start]))


@utils.part
def part_2_bfs():
    grid = utils.get_grid(cast=str, delimiter='', parse_graph=False)
    starts = [point for point in grid if grid[point] in {'S', 'a'}]
    print(shortest_path_to_end(grid, starts))


def shortest_paths_from_end(grid):
    end, _ = utils.assert_one(grid.items(), key=lambda item: item[1] == 'E')
    seen = set([end])
    queue = collections.deque([(point, 0) for point in seen])

    while queue:
        point, distance = queue.popleft()
        if grid[point] in {'S',  'a'}:
            return distance

        for neighbor in point.neighbors():
            if (
                neighbor in grid and
                neighbor not in seen and
                HEIGHTS[grid[point]] <= HEIGHTS[grid[neighbor]] + 1
            ):
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))


@utils.part
def part_2_bfs_reverse():
    grid = utils.get_grid(cast=str, delimiter='', parse_graph=False)
    print(shortest_paths_from_end(grid))
