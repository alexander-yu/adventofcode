import click
import networkx as nx

import utils


def path_count(graph, start, visited, can_visit_dupe):
    visited = visited | {start}
    count = 0

    if start == 'end':
        return 1

    for neighbor in graph.neighbors(start):
        if not neighbor.islower() or neighbor not in visited:
            count += path_count(graph, neighbor, visited, can_visit_dupe)
        elif neighbor != 'start' and neighbor.islower() and can_visit_dupe:
            count += path_count(graph, neighbor, visited, False)

    return count


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    edges = utils.get_input(__file__, delimiter='-', cast=str)
    graph = nx.Graph(edges)
    print(path_count(graph, 'start', set(), False))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    edges = utils.get_input(__file__, delimiter='-', cast=str)
    graph = nx.Graph(edges)
    print(path_count(graph, 'start', set(), True))


if __name__ == '__main__':
    cli()