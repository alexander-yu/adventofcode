import click
import networkx as nx

import utils


def get_graph():
    edges = utils.get_input(__file__, delimiter=')', cast=str)
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    graph = get_graph()
    source = 'COM'
    print(sum(nx.shortest_path_length(graph, source=source).values()))


@utils.part(cli)
def part_2():
    graph = get_graph()
    # YOU and SAN are not orbited by any other object, meaning that their only edge for each of them
    # is to the object they are each orbiting
    source = next(iter(graph['YOU']))
    target = next(iter(graph['SAN']))
    print(nx.shortest_path_length(graph, source=source, target=target))
