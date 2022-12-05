import collections
import enum

import networkx as nx
import numpy as np

import utils

from problems_2019 import intcode


class Direction(enum.Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Status(enum.Enum):
    WALL_HIT = 0
    MOVE_SUCCESS = 1
    OXYGEN_FOUND = 2


class PositionType(enum.Enum):
    UNKNOWN = 0
    EMPTY = 1
    WALL = 2
    OXYGEN = 3


VECTORS = {
    (0, 1): Direction.NORTH,
    (0, -1): Direction.SOUTH,
    (-1, 0): Direction.WEST,
    (1, 0): Direction.EAST
}

POSITION_DISPLAYS = {
    PositionType.UNKNOWN: ' ',
    PositionType.EMPTY: '.',
    PositionType.WALL: '#',
    PositionType.OXYGEN: 'O',
}


def display(graph):
    min_x = min(position[0] for position in graph.nodes)
    max_x = max(position[0] for position in graph.nodes)
    min_y = min(position[1] for position in graph.nodes)
    max_y = max(position[1] for position in graph.nodes)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) == (0, 0):
                print('S', end='')
            else:
                position_type = graph.nodes[(x, y)]['type'] if (x, y) in graph.nodes else PositionType.UNKNOWN
                print(POSITION_DISPLAYS[position_type], end='')

        print()


def explore():
    memory = utils.get_input(__file__)[0]
    droid = intcode.Program(memory, output_mode=intcode.OutputMode.PIPE)

    oxygen = None
    graph = nx.Graph()
    queue = collections.deque()

    graph.add_node((0, 0), type=PositionType.EMPTY)
    queue.append(((0, 0), droid.copy()))

    while queue:
        node, droid = queue.popleft()
        for vector, direction in VECTORS.items():
            neighbor = tuple(np.array(node) + vector)
            if neighbor not in graph.nodes:
                droid_copy = droid.copy()
                status, _ = droid_copy.run(direction.value)
                status = Status(status)
                graph.add_node(neighbor)
                graph.add_edge(node, neighbor)

                if status == Status.WALL_HIT:
                    graph.nodes[neighbor]['type'] = PositionType.WALL
                    continue
                elif status == Status.OXYGEN_FOUND:
                    graph.nodes[neighbor]['type'] = PositionType.OXYGEN
                    oxygen = neighbor
                else:
                    graph.nodes[neighbor]['type'] = PositionType.EMPTY

                queue.append((neighbor, droid_copy))

    return graph, oxygen


@utils.part
def part_1():
    graph, oxygen_position = explore()
    print(len(nx.shortest_path(graph, source=(0, 0), target=oxygen_position)) - 1)


@utils.part
def part_2():
    graph, oxygen_position = explore()
    print(max(nx.shortest_path_length(graph, source=oxygen_position).values()) - 1)
