import click

from boltons import iterutils

import utils


class Cups:
    def __init__(self, cups):
        self.nodes = {}

        for cup in cups:
            self.nodes[cup] = Node(cup)

        for i, cup in enumerate(cups):
            node = self.nodes[cup]
            node.prev = self.nodes[cups[(i - 1) % len(cups)]]
            node.next = self.nodes[cups[(i + 1) % len(cups)]]

    def get_node(self, cup):
        return self.nodes[cup]

    def insert(self, destination, nodes):
        for node in nodes:
            node.prev = destination
            node.next = destination.next
            destination.next.prev = node
            destination.next = node
            destination = node
            self.nodes[node.value] = node

    def remove(self, nodes):
        for node in nodes:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = None
            node.next = None
            self.nodes.pop(node.value)

    def values(self, start_cup):
        values = [start_cup]
        node = self.nodes[start_cup].next

        while node.value != start_cup:
            values.append(node.value)
            node = node.next

        return values

    def __getitem__(self, cup):
        return self.nodes[cup]

    def __contains__(self, cup):
        return cup in self.nodes

    def __iter__(self):
        for cup in self.nodes:
            yield cup


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


def play(cups, rounds):
    starting_cup = cups[0]
    cups = Cups(cups)
    node = cups[starting_cup]
    min_cup = min(cups)
    max_cup = max(cups)

    for _ in range(rounds):
        removed_nodes = node.next, node.next.next, node.next.next.next
        removed_cups = [node.value for node in removed_nodes]
        cups.remove(removed_nodes)

        destination = node.value - 1
        while destination not in cups:
            # pylint: disable=cell-var-from-loop
            destination -= 1
            new_min_cup = iterutils.first(
                range(min_cup, min_cup + 4),
                key=lambda cup: cup not in removed_cups,
            )
            new_max_cup = iterutils.first(
                range(max_cup, max_cup - 4, -1),
                key=lambda cup: cup not in removed_cups,
            )

            if destination < new_min_cup:
                destination = new_max_cup

        destination = cups.get_node(destination)
        cups.insert(destination, removed_nodes)
        node = node.next

    return cups


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    cups = utils.get_input(__file__, delimiter='')[0]
    cups = play(cups, 100)
    print(''.join(str(value) for value in cups.values(1)[1:]))


@utils.part(cli)
def part_2():
    cups = utils.get_input(__file__, delimiter='')[0]
    cups += list(range(max(cups) + 1, 1_000_001))
    cups = play(cups, 10_000_000)
    cup_1, cup_2 = cups.values(1)[1:3]
    print(cup_1 * cup_2)


if __name__ == '__main__':
    cli()
