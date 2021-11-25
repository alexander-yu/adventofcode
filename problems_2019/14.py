import collections
import fractions
import itertools
import re

import click
import networkx as nx

import utils


ONE_TRILLION = 1_000_000_000_000


def get_ore_required(fuel_required):
    graph = get_graph()
    graph.nodes['FUEL']['min_required'] = fuel_required

    for product in nx.topological_sort(graph):
        quantity = graph.nodes[product].get('quantity')
        if not quantity:
            continue

        min_product = graph.nodes[product]['min_required']
        increments = min_product // quantity + (min_product % quantity != 0)
        for reactant in graph.successors(product):
            edge = graph.edges[product, reactant]
            graph.nodes[reactant]['min_required'] += increments * edge['reactant']

    return graph.nodes['ORE']['min_required']


def get_graph():
    graph = nx.DiGraph()

    for reaction in utils.get_input(__file__, delimiter=' => ', cast=str, test=False):
        reactants, product = reaction
        product_quantity, product = product.split()

        for reactant in reactants.split(', '):
            quantity, reactant = reactant.split()
            graph.add_edge(
                product,
                reactant,
                reactant=int(quantity),
            )
            graph.nodes[product]['quantity'] = int(product_quantity)
            graph.nodes[product]['min_required'] = 0
            graph.nodes[reactant]['min_required'] = 0

    return graph


def argmax(f, limit):
    x = 0
    exp = 0
    upper = float('inf')

    while True:
        y = f(x)
        if y < limit:
            if upper == x + 1:
                return x
            elif upper == float('inf'):
                exp += 1
            else:
                exp = (upper - x).bit_length() - 2

            x += int(2 ** exp)
        elif y > limit:
            upper = x
            exp = max(exp - 1, 0)
            x -= int(2 ** exp)
        else:
            return x


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    print(get_ore_required(1))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    print(argmax(get_ore_required, ONE_TRILLION))


if __name__ == '__main__':
    cli()
