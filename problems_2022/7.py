from typing import List

import dataclasses

import parse

import utils


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Node:
    name: str
    parent: 'Node'
    children: List['Node'] = dataclasses.field(default_factory=list)
    files: List[File] = dataclasses.field(default_factory=list)
    size: int = 0


def get_tree():
    data = utils.get_input(cast=str, delimiter='\n', line_delimiter='\n$ ', remove_prefix='$ ')
    root = Node('/', None)
    pointer = root

    for cmd, *output in data:
        if cmd.startswith('ls'):
            for child in output:
                if child.startswith('dir'):
                    pointer.children.append(Node(child[4:], pointer))
                else:
                    size, name = parse.parse('{:d} {}', child)
                    pointer.files.append(File(name, size))
        else:
            folder = cmd[3:]

            if folder == '/':
                pointer = root
            elif folder == '..':
                pointer = pointer.parent
            else:
                pointer = next(child for child in pointer.children if child.name == folder)

    set_sizes(root)
    return root


def set_sizes(node):
    total = sum(set_sizes(child) for child in node.children) + sum(file.size for file in node.files)
    node.size = total
    return total


def get_small_nodes(node, threshold):
    small_nodes = []

    for child in node.children:
        small_nodes.extend(get_small_nodes(child, threshold))

    if node.size < threshold:
        small_nodes.append(node)

    return small_nodes


def min_to_delete(node, min_so_far, threshold):
    for child in node.children:
        min_node = min_to_delete(child, min_so_far, threshold)

        if min_node.size < min_so_far.size:
            min_so_far = min_node

    if threshold <= node.size < min_so_far.size:
        min_so_far = node

    return min_so_far


@utils.part
def part_1():
    root = get_tree()
    dirs = get_small_nodes(root, 100000)
    print(sum(node.size for node in dirs))


@utils.part
def part_2():
    root = get_tree()
    threshold = root.size - 40000000
    node = min_to_delete(root, root, threshold)
    print(node.size)
