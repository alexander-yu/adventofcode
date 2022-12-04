import re

import cachetools
import click
import networkx as nx

import utils

BAG_REGEX = r'(?P<color>[a-z]+ [a-z]+) bags?'
WEIGHT_REGEX = rf'(?P<weight>\d+) {BAG_REGEX}'
EMPTY = 'no other bags'


def add_rule(graph, bag, components):
    if components == EMPTY:
        graph.add_node(bag)
    else:
        components = components.split(', ')
        for component in components:
            match = re.match(WEIGHT_REGEX, component)
            color, weight = match.group('color'), match.group('weight')
            graph.add_edge(bag, color, weight=int(weight))


def get_graph():
    rules = utils.get_input(__file__, delimiter=' contain ', cast=str, rstrip='.')
    graph = nx.DiGraph()
    for bag, components in rules:
        bag = re.match(BAG_REGEX, bag).group('color')
        add_rule(graph, bag, components)

    return graph


@cachetools.cached({}, key=lambda _, bag: bag)
def get_size(graph, bag):
    return sum([
        graph.edges[bag, component]['weight'] * (1 + get_size(graph, component))
        for component in graph.successors(bag)
    ])


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    graph = get_graph()
    print(len(nx.single_target_shortest_path(graph, 'shiny gold')) - 1)


@cli.command
@utils.part
def part_2():
    graph = get_graph()
    print(get_size(graph, 'shiny gold'))


if __name__ == '__main__':
    cli()
