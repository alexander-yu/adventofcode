import collections
import enum
import heapq
import string

import cachetools
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

BOT_VECTORS = [
    np.array([1, 1]),
    np.array([1, -1]),
    np.array([-1, 1]),
    np.array([-1, -1]),
]


class PointType(utils.MultiValueEnum):
    EMPTY = '.'
    WALL = '#'
    ENTRANCE = '@'
    KEY = tuple(string.ascii_lowercase)
    DOOR = tuple(string.ascii_uppercase)


class Graph:
    def __init__(self, graph, keys):
        self.graph = graph
        self.key_map = {key: i for i, key in enumerate(keys)}
        self.cache = {}

    @cachetools.cachedmethod(lambda self: self.cache)
    def reachable_keys(self, start, keys):
        queue = collections.deque([(start, 0)])
        visited = set()

        while queue:
            position, moves = queue.popleft()
            point = self.graph.nodes[position]['value']
            if PointType(point) == PointType.KEY and not keys & 1 << self.key_map[point]:
                yield (position, point, moves)
                continue

            for neighbor in self.graph.neighbors(position):
                if neighbor not in visited:
                    visited.add(neighbor)
                    point = self.graph.nodes[neighbor]['value']
                    point_type = PointType(point)

                    if point_type == PointType.DOOR and not keys & 1 << self.key_map[point.lower()]:
                        continue

                    queue.append((neighbor, moves + 1))


def get_graph(single_bot=True):
    graph = nx.Graph()

    points = {}
    keys = []
    entrance = None
    x, y = 0, 0

    for line in utils.get_input(__file__, delimiter='', cast=str):
        for point in line:
            points[(x, y)] = point

            if PointType(point) == PointType.ENTRANCE:
                entrance = (x, y)

            x += 1

        x = 0
        y -= 1

    if not single_bot:

        for vector in VECTORS:
            new_wall = tuple(np.array(entrance) + vector)
            points[new_wall] = PointType.WALL.value

        for vector in BOT_VECTORS:
            new_bot = tuple(np.array(entrance) + vector)
            points[new_bot] = PointType.ENTRANCE.value

        points[entrance] = PointType.WALL.value

    entrances = []
    for coordinate, point in points.items():
        point_type = PointType(point)
        if point_type != PointType.WALL:
            graph.add_node(coordinate, value=point)

        if point_type == PointType.KEY:
            keys.append(point)
        elif point_type == PointType.ENTRANCE:
            entrances.append(coordinate)

    for coordinate in graph.nodes:
        for vector in VECTORS:
            neighbor = tuple(np.array(coordinate) + vector)
            if neighbor in graph.nodes:
                graph.add_edge(coordinate, neighbor)

    return Graph(graph, sorted(keys)), entrances


def get_distance(graph, entrances, bots=1):
    heap = [(0, entrances, 0)]
    seen = [set() for _ in range(bots)]
    all_keys = (1 << len(graph.key_map)) - 1
    while heap:
        moves, positions, keys = heapq.heappop(heap)
        if keys == all_keys:
            return moves

        for i, position in enumerate(positions):
            if (position, keys) in seen:
                continue
            seen[i].add((position, keys))
            for key_position, key, distance in graph.reachable_keys(position, keys):
                new_position = list(positions)
                new_position[i] = key_position
                heapq.heappush(heap, (moves + distance, tuple(new_position), keys | 1 << graph.key_map[key]))


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    graph, entrances = get_graph()
    print(get_distance(graph, entrances))


@cli.command
@utils.part
def part_2():
    graph, entrances = get_graph(single_bot=False)
    print(get_distance(graph, entrances, bots=4))


if __name__ == '__main__':
    cli()
