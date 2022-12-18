import collections
import dataclasses

import utils


def get_data():
    return utils.get_input(cast=int, line_cast=utils.Vector, delimiter=',', line_delimiter='\n')


class Boundary:
    def __init__(self, points):
        self.min_x = min(point[0] for point in points)
        self.min_y = min(point[1] for point in points)
        self.min_z = min(point[2] for point in points)
        self.max_x = max(point[0] for point in points)
        self.max_y = max(point[1] for point in points)
        self.max_z = max(point[2] for point in points)

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


def is_exterior(point, points, boundary, space):
    """
    To check if a point is in the exterior space surrounding the points,
    we perform a floodfill for the point.

    We make heavy use of caching here as well: for a given result, if
    we determine that a point is either in the interior or exterior,
    we update our current set of interior/exterior points with all of the
    points seen as part of the current floodfill execution.
    """
    if point in points or point in space.interior:
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

            if neighbor not in points and neighbor not in seen:
                queue.append(neighbor)
                seen.add(neighbor)

    space.interior.update(seen)
    return False


@utils.part
def part_1():
    points = set(get_data())

    print(sum(
        len([
            neighbor
            for neighbor in point.neighbors()
            if neighbor not in points
        ])
        for point in points
    ))


@utils.part
def part_2():
    points = frozenset(get_data())
    boundary = Boundary(points)
    space = Space()

    print(sum(
        len([
            neighbor
            for neighbor in point.neighbors()
            if is_exterior(neighbor, points, boundary, space)
        ])
        for point in points
    ))
