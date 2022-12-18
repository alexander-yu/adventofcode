import collections
import dataclasses
import itertools

import networkx as nx

from utils import Vector

import utils


def get_data():
    return utils.get_input(cast=int, line_cast=Vector, delimiter=',', line_delimiter='\n')


class Boundary:
    def __init__(self, cubes):
        self.min_x = min(point[0] for point in cubes)
        self.min_y = min(point[1] for point in cubes)
        self.min_z = min(point[2] for point in cubes)
        self.max_x = max(point[0] for point in cubes)
        self.max_y = max(point[1] for point in cubes)
        self.max_z = max(point[2] for point in cubes)

    def contains(self, point):
        x, y, z = point
        return all([
            self.min_x <= x <= self.max_x,
            self.min_y <= y <= self.max_y,
            self.min_z <= z <= self.max_z,
        ])


@dataclasses.dataclass
class Space:
    interior: set = dataclasses.field(default_factory=set)
    exterior: set = dataclasses.field(default_factory=set)


def is_exterior(point, cubes, boundary, space):
    """
    To check if a point is in the exterior space surrounding the cubes,
    we perform a floodfill for the point.

    We make heavy use of caching here as well: for a given result, if
    we determine that a point is either in the interior or exterior,
    we update our current set of interior/exterior points with all of the
    points seen as part of the current floodfill execution.
    """
    if point in cubes or point in space.interior:
        return False

    if point in space.exterior:
        return True

    queue = collections.deque([point])

    # We cache based on points that have been added to the queue rather than
    # by points that have been processed by the queue, to avoid adding duplicate
    # neighbors
    seen = set([point])

    while queue:
        point = queue.popleft()

        for neighbor in point.neighbors():
            # If the neighbor exceeds the boundary box, it's clearly an exterior point
            if neighbor in space.exterior or not boundary.contains(neighbor):
                space.exterior.update(seen)
                return True

            if neighbor in space.interior:
                space.interior.update(seen)
                return False

            if neighbor not in cubes and neighbor not in seen:
                queue.append(neighbor)
                seen.add(neighbor)

    space.interior.update(seen)
    return False


@utils.part
def part_1():
    cubes = set(get_data())

    print(sum(
        len([
            neighbor
            for neighbor in cube.neighbors()
            if neighbor not in cubes
        ])
        for cube in cubes
    ))


@utils.part
def part_2():
    cubes = set(get_data())
    boundary = Boundary(cubes)
    space = Space()

    print(sum(
        len([
            neighbor
            for neighbor in cube.neighbors()
            if is_exterior(neighbor, cubes, boundary, space)
        ])
        for cube in cubes
    ))


@utils.part
def part_2_connected_components():
    cubes = set(get_data())
    boundary = Boundary(cubes)
    graph = nx.Graph()

    # We create a bounding box with at least one layer of space between it and the cubes to make sure that
    # the exterior completely surrounds the cubes
    for x, y, z in itertools.product(
        range(boundary.min_x - 1, boundary.max_x + 2),
        range(boundary.min_y - 1, boundary.max_y + 2),
        range(boundary.min_z - 1, boundary.max_z + 2),
    ):
        point = Vector(x, y, z)
        for neighbor in point.neighbors():
            if point not in cubes and neighbor not in cubes:
                graph.add_edge(point, neighbor)

    # This is guaranteed to be an exterior point since by definition it's not contained in the set of cubes
    exterior_corner = Vector(boundary.min_x - 1, boundary.min_y - 1, boundary.min_z - 1)
    exterior = set(nx.descendants(graph, exterior_corner))

    print(sum(
        len([
            neighbor
            for neighbor in cube.neighbors()
            if neighbor in exterior
        ])
        for cube in cubes
    ))
