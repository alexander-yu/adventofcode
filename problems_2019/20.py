import collections
import itertools
import string

import networkx as nx

from boltons import iterutils

from utils import Vector

import utils


VECTORS = [
    Vector(0, 1, 0),
    Vector(0, -1, 0),
    Vector(1, 0, 0),
    Vector(-1, 0, 0),
]


class Direction(utils.MultiValueEnum):
    HORIZONTAL = VECTORS[0], VECTORS[1]
    VERTICAL = VECTORS[2], VECTORS[3]


class PointType(utils.MultiValueEnum):
    EMPTY = '.'
    WALL = '#'
    LETTER = tuple(string.ascii_uppercase)
    SPACE = ' '


class Label:
    def __init__(self, name, position, letter_positions):
        self.name = name
        self.position = position
        self.letter_positions = letter_positions


def is_letter(graph, position):
    if position not in graph.nodes:
        return False
    return PointType(graph.nodes[position]['value']) == PointType.LETTER


def is_empty(graph, position):
    if position not in graph.nodes:
        return False
    return PointType(graph.nodes[position]['value']) == PointType.EMPTY


def is_outer_portal(width, height, portal):
    return portal[0] in [2, width - 3] or portal[1] in [-2, -1 * height + 3]


def get_label(graph, first_letter):
    # Either down or right
    second_letter_vectors = [
        VECTORS[1], VECTORS[2]
    ]

    for vector in second_letter_vectors:
        neighbor = first_letter + vector
        if is_letter(graph, neighbor):
            label_position = None
            candidate_positions = [
                first_letter - vector,
                neighbor + vector,
            ]
            for position in candidate_positions:
                if is_empty(graph, position):
                    label_position = position

            if label_position:
                label = graph.nodes[first_letter]['value'] + graph.nodes[neighbor]['value']
                return Label(label, label_position, [first_letter, neighbor])

    return None


def get_graph(levels=1):
    graph = nx.Graph()

    points = {}
    letters = set()
    x, y = 0, 0
    width, height = 0, 0

    for line in utils.get_input(delimiter='', cast=str):
        for point in line:
            points[(x, y)] = point
            if PointType(point) == PointType.LETTER:
                letters.add((x, y, 0))

            x += 1
            width = max(width, x)

        x = 0
        y -= 1
        height = max(height, abs(y))

    for coordinate, point in points.items():
        if PointType(point) not in [PointType.WALL, PointType.SPACE]:
            for i in range(levels):
                graph.add_node(coordinate + (i,), value=point)

    labels = collections.defaultdict(list)
    while letters:
        first_letter = letters.pop()
        label = get_label(graph, first_letter)

        if not label:
            # This is not actually a first letter
            continue

        labels[label.name].append(label.position)

        for letter_position in label.letter_positions:
            letters.discard(letter_position)

        for i in range(levels):
            for letter_position in label.letter_positions:
                graph.remove_node(letter_position[:-1] + (i,))

            graph.add_node(label.position[:-1] + (i,), value=label.name)

    for positions in labels.values():
        for pad_1, pad_2 in itertools.combinations(positions, 2):
            if levels == 1:
                graph.add_edge(pad_1, pad_2)
            else:
                if is_outer_portal(width, height, pad_1):
                    outer_portal, inner_portal = pad_1, pad_2
                else:
                    outer_portal, inner_portal = pad_2, pad_1

                for prev_level, next_level in iterutils.pairwise(range(levels)):
                    graph.add_edge(
                        inner_portal[:-1] + (prev_level,),
                        outer_portal[:-1] + (next_level,),
                    )

    for coordinate in graph.nodes:
        for vector in VECTORS:
            neighbor = Vector(coordinate + vector)
            if neighbor in graph.nodes:
                graph.add_edge(coordinate, neighbor)

    start, end = labels['AA'][0], labels['ZZ'][0]

    return graph, start, end


@utils.part
def part_1():
    graph, start, end = get_graph()
    print(nx.shortest_path_length(graph, source=start, target=end))


@utils.part
def part_2():
    max_recursion_depth = 30
    graph, start, end = get_graph(levels=max_recursion_depth)
    print(nx.shortest_path_length(graph, source=start, target=end))
