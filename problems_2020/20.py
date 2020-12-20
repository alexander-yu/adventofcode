import collections
import itertools
import math
import re

from dataclasses import dataclass

import click
import networkx as nx
import numpy as np

from boltons import iterutils

import utils


EDGE_TO_VECTOR = {
    0: (0, -1),  # left
    1: (-1, 0),  # top
    2: (0, 1),  # right
    3: (1, 0),  # bottom
}

SEA_MONSTER_REGEXES = [
    r'..................#.',
    r'#....##....##....###',
    r'.#..#..#..#..#..#...',
]
SEA_MONSTER_SIZE = sum(regex.count('#') for regex in SEA_MONSTER_REGEXES)


@dataclass
class Tile:
    id: int
    points: np.ndarray

    def edges(self):
        edges = [
            self.points[:, 0][::-1],  # left
            self.points[0],  # top
            self.points[:, -1],  # right
            self.points[-1][::-1],  # bottom
        ]
        return [''.join(edge) for edge in edges]

    @staticmethod
    def parse(header, points):
        tile_id = int(header.split(' ')[-1].rstrip(':'))
        return Tile(tile_id, points)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.points)

    def rotate(self, k=1):
        self.points = rotate(self.points, k=k)

    def flip(self):
        self.points = flip(self.points)

    def clone(self):
        return Tile(self.id, self.points[:])


def rotate(points, k=1):
    # Rotate clockwise
    return np.rot90(points, k=k, axes=(1, 0))


def flip(points):
    return np.fliplr(points)


def get_tiles():
    return [
        Tile.parse(
            tile[0],
            np.array([list(row) for row in tile[1:]]),
        )
        for tile in utils.get_input(
            __file__,
            cast=str,
            delimiter='\n',
            line_delimiter='\n\n',
        )
    ]


def get_tile_graph(tiles):
    graph = nx.Graph()
    edges = collections.defaultdict(list)

    for tile in tiles:
        graph.add_node(tile.id, tile=tile)

        for edge in tile.edges():
            edges[edge].append(tile.id)
            edges[edge[::-1]].append(tile.id)

    for edge, tile_ids in edges.items():
        for tile_1, tile_2 in itertools.combinations(tile_ids, 2):
            graph.add_edge(tile_1, tile_2, edge=[edge, edge[::-1]])

    return graph


def set_top_left_corner(graph):
    # Start with an arbitrary corner, make this the top-left corner
    corner = iterutils.first(node for node in graph.nodes if graph.degree(node) == 2)
    corner_tile = graph.nodes[corner]['tile']

    interior_edges = set(
        itertools.chain.from_iterable(
            graph.edges[edge]['edge']
            for edge in graph.edges(corner)
        )
    )

    corner_edges = corner_tile.edges()
    interior_indices = sorted([i for i, edge in enumerate(corner_edges) if edge in interior_edges])

    # Rotate corner until it's in place (i.e. the interior borders face to the right and below)
    while interior_indices != [2, 3]:
        corner_tile.rotate()
        corner_edges = corner_tile.edges()
        interior_indices = sorted([i for i, edge in enumerate(corner_edges) if edge in interior_edges])

    return corner


def orient_tile_to_edge(tile_1, edge_1, tile_2):
    # Rotate and/or flip tile_2 until it matches edge_1 on tile_1
    for rotations, should_flip in itertools.product(range(4), [True, False]):
        temp_tile = tile_2.clone()
        temp_tile.rotate(k=rotations)
        if should_flip:
            temp_tile.flip()

        # edge_2 must be equal to edge_1 + 2 mod 4, and the edge_2 must be the reverse of edge_1
        if temp_tile.edges()[(edge_1 + 2) % 4][::-1] == tile_1.edges()[edge_1]:
            tile_2.points = temp_tile.points
            break


def assemble_tiles(graph):
    corner = set_top_left_corner(graph)
    positions = {corner: (0, 0)}

    for edge in nx.bfs_edges(graph, corner):
        # pylint: disable=cell-var-from-loop
        edges = graph.edges[edge]['edge']
        tile_id_1, tile_id_2 = edge
        tile_1, tile_2 = graph.nodes[tile_id_1]['tile'], graph.nodes[tile_id_2]['tile']

        assert tile_id_1 in positions

        tile_1_edges = tile_1.edges()
        edge_1 = iterutils.first(range(4), key=lambda i: tile_1_edges[i] in edges)
        positions[tile_id_2] = utils.add_vector(positions[tile_id_1], EDGE_TO_VECTOR[edge_1])
        orient_tile_to_edge(tile_1, edge_1, tile_2)

    # Now that positions have been determined, form grid of sub-images
    dims = utils.add_vector(max(positions.values()), (1, 1))
    grid = [
        [None for _ in range(dims[1])]
        for _ in range(dims[0])
    ]

    for tile_id, (i, j) in positions.items():
        tile = graph.nodes[tile_id]['tile']
        grid[i][j] = tile
        # Truncate tile borders
        tile.points = tile.points[1:-1, 1:-1]

    # Merge truncated tiles into final image
    return np.vstack([
        np.hstack([tile.points for tile in row])
        for row in grid
    ])


def get_sea_monsters(image):
    sea_monsters = 0

    for i, j in itertools.product(range(image.shape[0] - 2), range(image.shape[1] - 19)):
        lines = [''.join(line) for line in image[i:i + 3, j:j + 20]]
        if all(re.fullmatch(regex, line) for line, regex in zip(lines, SEA_MONSTER_REGEXES)):
            sea_monsters += 1

    return sea_monsters


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    graph = get_tile_graph(get_tiles())
    corners = [node for node in graph.nodes if graph.degree(node) == 2]
    print(math.prod(corners))


@cli.command()
def part_2():
    graph = get_tile_graph(get_tiles())
    image = assemble_tiles(graph)

    for rotations, should_flip in itertools.product(range(4), [True, False]):
        new_image = rotate(image, rotations)
        if should_flip:
            new_image = flip(new_image)

        sea_monsters = get_sea_monsters(new_image)
        if sea_monsters:
            print((new_image == '#').sum() - SEA_MONSTER_SIZE * sea_monsters)
            break


if __name__ == '__main__':
    cli()
