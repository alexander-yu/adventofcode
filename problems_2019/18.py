import collections
import enum
import string

import click
import networkx as nx
import numpy as np

import utils

VECTORS = [
    np.array([0, 1]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([-1, 0]),
]


class MultiValueEnum(enum.Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj


class PointType(MultiValueEnum):
    EMPTY = '.'
    WALL = '#'
    ENTRANCE = '@'
    KEY = tuple(string.ascii_lowercase)
    DOOR = tuple(string.ascii_uppercase)


def get_graph():
    graph = nx.Graph()

    points = {}
    x, y = 0, 0

    for line in utils.get_input(__file__, delimiter='', cast=str):
        for point in line:
            points[(x, y)] = point
            x += 1

        x = 0
        y -= 1

    for coordinate, point in points.items():
        graph.add_node(coordinate, value=point)

    for coordinate in points:
        for vector in VECTORS:
            neighbor = tuple(np.array(coordinate) + vector)
            if neighbor in graph.nodes and PointType(graph.nodes[neighbor]['value']) != PointType.WALL:
                graph.add_edge(coordinate, neighbor)

    return graph


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    graph = get_graph()
    print(graph.nodes(data=True))


@cli.command()
def part_2():
    pass


if __name__ == '__main__':
    cli()
