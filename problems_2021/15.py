import networkx as nx
import numpy as np

import utils


def get_lowest_risk_path(grid):
    start = (0, 0)
    end = (grid.rows - 1, grid.columns - 1)

    for u, v in grid.graph.edges():
        grid.graph.edges[u, v]['risk'] = grid[v]

    return nx.dijkstra_path_length(grid.graph, start, end, weight='risk')


def expand_map(points):
    points = np.array(points)
    return np.vstack([
        np.hstack([
            (points + i + j) - 9 * ((points + i + j) > 9)
            for i in range(5)
        ])
        for j in range(5)
    ])


@utils.part
def part_1():
    grid = utils.get_grid(grid_cls=utils.DirectedGrid, delimiter='')
    print(get_lowest_risk_path(grid))


@utils.part
def part_2():
    grid = utils.get_grid(input_transformer=expand_map, grid_cls=utils.DirectedGrid, delimiter='')
    print(get_lowest_risk_path(grid))
