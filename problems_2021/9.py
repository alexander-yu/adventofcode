import collections
import math

import click
import networkx as nx

import utils


def get_low_points(grid):
    for point, value in grid.items():
        if all(
            grid[neighbor] > value
            for neighbor in grid.neighbors(point)
        ):
            yield point


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    grid = utils.get_grid(__file__, delimiter='')
    print(sum(grid[point] + 1 for point in get_low_points(grid)))


@utils.part(cli)
def part_2():
    grid = utils.get_grid(__file__, delimiter='')

    # We remove all nodes of maximal height from the original graph. This will partition
    # the grid into connected components, where the connected components are precisely
    # the basins.
    for point, value in grid.items():
        if value == 9:
            grid.graph.remove_node(point)

    basins = nx.connected_components(grid.graph)
    top_3 = sorted(basins, key=len, reverse=True)[:3]
    print(math.prod(len(basin) for basin in top_3))


@utils.part(cli)
def part_2_bfs():
    grid = utils.get_grid(__file__, delimiter='')

    # We find all low points like in part 1, but perform a classic flood fill algorithm
    # via BFS starting from low points, and filling it upwards.
    #
    # Each fill from a low point will be guaranteed to consist of a single basin,
    # since we can assume that every node not maximum height is only part of 1 basin.
    basins = []
    for low_point in get_low_points(grid):
        queue = collections.deque([low_point])
        basin = set([low_point])
        visited = set([low_point])

        while queue:
            point = queue.popleft()

            for neighbor in grid.neighbors(point):
                if neighbor not in visited:
                    visited.add(neighbor)

                    if grid[neighbor] != 9:
                        basin.add(neighbor)
                        queue.append(neighbor)

        basins.append(basin)

    top_3 = sorted(basins, key=len, reverse=True)[:3]
    print(math.prod(len(basin) for basin in top_3))


@utils.part(cli)
def part_2_dag():
    grid = utils.get_grid(__file__, delimiter='')

    # We find all low points like in part 1, but create a directed downflow graph,
    # where u -> v is a directed edge if there is downwards flow from u to v, and u
    # is not a node of maximal height.
    #
    # For a given low point, it will be a part of a DAG such that the low point
    # will be the singular leaf node of the DAG. Thus, the corresponding basin
    # will simply be all nodes in the DAG that can reach the low point as well as
    # the low point itself.
    downflow_graph = nx.DiGraph()

    for point in grid:
        for neighbor in grid.neighbors(point):
            if grid[point] != 9 and grid[point] > grid[neighbor]:
                downflow_graph.add_edge(point, neighbor)

    basins = []
    for low_point in get_low_points(grid):
        basin = set([low_point]) | nx.ancestors(downflow_graph, low_point)
        basins.append(basin)

    top_3 = sorted(basins, key=len, reverse=True)[:3]
    print(math.prod(len(basin) for basin in top_3))


if __name__ == '__main__':
    cli()
