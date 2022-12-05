import re

import networkx as nx
import regex

import utils


def add_rule(graph, rule, skip=None):
    number, rule = rule.split(':')

    if skip and number in skip:
        return graph

    rule = rule.strip().split(' ')

    if len(rule) == 1 and rule[0].startswith('"'):
        # Remove quotes for leaf nodes
        graph.add_node(number, rule=rule[0].strip('"'))
    else:
        graph.add_node(number, rule=rule)

        # For each dependency in the rule, add a directed edge
        # from the dependency to the rule
        for term in rule:
            if term != '|':
                graph.add_edge(term, number)

    return graph


def resolve(graph):
    # Resolve the rules in the graph by iterating through a topologically sorted
    # list of the nodes, so that dependencies are resolved first
    for node in nx.topological_sort(graph):
        rule = graph.nodes[node]['rule']
        if isinstance(rule, list):
            for i, term in enumerate(rule):
                if term != '|':
                    term_rule = graph.nodes[term]['rule']
                    rule[i] = fr'(?:{term_rule})'

            graph.nodes[node]['rule'] = ''.join(rule)


@utils.part
def part_1():
    rules, messages = utils.get_input(__file__, cast=str, delimiter='\n', line_delimiter='\n\n')
    graph = nx.DiGraph()

    for rule in rules:
        graph = add_rule(graph, rule)

    resolve(graph)

    rule_0 = graph.nodes['0']['rule']
    print(len([message for message in messages if re.fullmatch(rule_0, message)]))


@utils.part
def part_2():
    rules, messages = utils.get_input(__file__, cast=str, delimiter='\n', line_delimiter='\n\n')
    graph = nx.DiGraph()

    for rule in rules:
        # Skip rules 0, 8, and 11; we manually handle those
        graph = add_rule(graph, rule, skip={'0', '8', '11'})

    resolve(graph)

    rule_31 = graph.nodes['31']['rule']
    rule_42 = graph.nodes['42']['rule']

    # Use a recursive regex here
    rule_0 = fr'(?:{rule_42})+((?:{rule_42})(|(?1))(?:{rule_31}))'
    print(len([message for message in messages if regex.fullmatch(rule_0, message)]))
