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
