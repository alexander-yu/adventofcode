import dataclasses
import heapq
import typing

import click
import numpy as np

import utils


A, B, C, D = 10 ** np.arange(4)

ROOM_DOORS = {
    A: 2,
    B: 4,
    C: 6,
    D: 8,
}

ROOMS = {
    A: 0,
    B: 1,
    C: 2,
    D: 3,
}


@dataclasses.dataclass(frozen=True)
class Room:
    type: int
    size: int
    amphipods: tuple[int]

    def is_final(self):
        return len(self.amphipods) == self.size and all(amphipod == self.type for amphipod in self.amphipods)

    def is_enterable(self):
        return len(self.amphipods) < self.size and all(amphipod == self.type for amphipod in self.amphipods)

    def __len__(self):
        return len(self.amphipods)

    def pop(self):
        if not self.amphipods:
            raise ValueError('Room is empty')

        return self.amphipods[-1], dataclasses.replace(self, amphipods=self.amphipods[:-1])

    def append(self, amphipod):
        return dataclasses.replace(self, amphipods=self.amphipods + (amphipod,))

    def gap(self):
        return self.size - len(self.amphipods)


@dataclasses.dataclass(frozen=True)
class Hallway:
    spaces: tuple[typing.Optional[int]] = (None,) * 11
    DOORS: typing.ClassVar = set(ROOM_DOORS.values())

    def __iter__(self):
        return iter(self.spaces)

    def get_valid_moves(self, start):
        left_range = range(start - 1, -1, -1)
        right_range = range(start + 1, 11, 1)

        for search_range in [left_range, right_range]:
            for space in search_range:
                if space in self.DOORS:
                    continue

                if self.spaces[space] is not None:
                    break

                distance = abs(start - space)
                yield (space, distance)

    def is_clear(self, start, stop):
        if start < stop:
            search_range = range(start + 1, stop + 1)
        else:
            search_range = range(stop, start)

        return all(self.spaces[space] is None for space in search_range)

    def update_space(self, space, amphipod):
        return Hallway(self.spaces[:space] + (amphipod,) + self.spaces[space + 1:])


@dataclasses.dataclass(frozen=True)
class State:
    energy: int
    rooms: tuple[Room]
    hallway: Hallway

    def __hash__(self):
        return hash((self.rooms, self.hallway))

    def __eq__(self, other):
        return isinstance(other, State) and hash(self) == hash(other)

    def __lt__(self, other):
        return self.energy < other.energy

    def is_final(self):
        return all(room.is_final() for room in self.rooms)

    def update_room(self, i, new_room):
        return self.rooms[:i] + (new_room,) + self.rooms[i + 1:]


def get_best_path(initial_state):
    heap = [initial_state]
    visited = set()

    while heap:
        state = heapq.heappop(heap)
        if state.is_final():
            return state.energy
        if state in visited:
            continue

        visited.add(state)

        # Generate all next states where an amphipod moves into a hallway
        for i, room in enumerate(state.rooms):
            if room and not room.is_final():
                amphipod, new_room = room.pop()
                door = ROOM_DOORS[room.type]

                for space, distance in state.hallway.get_valid_moves(door):
                    new_state = State(
                        state.energy + (room.gap() + 1 + distance) * amphipod,
                        state.update_room(i, new_room),
                        state.hallway.update_space(space, amphipod),
                    )
                    if new_state not in visited:
                        heapq.heappush(heap, new_state)

        # Generate all next states where an amphipod moves into a room
        for space, amphipod in enumerate(state.hallway):
            if amphipod is None:
                continue

            door = ROOM_DOORS[amphipod]
            room_idx = ROOMS[amphipod]
            room = state.rooms[room_idx]

            if state.hallway.is_clear(space, door) and room.is_enterable():
                new_room = room.append(amphipod)
                distance = abs(door - space)

                new_state = State(
                    state.energy + (distance + room.gap()) * amphipod,
                    state.update_room(room_idx, new_room),
                    state.hallway.update_space(space, None),
                )
                if new_state not in visited:
                    heapq.heappush(heap, new_state)


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    energy = get_best_path(State(
        0,
        (
            Room(A, 2, (C, D)),
            Room(B, 2, (C, B)),
            Room(C, 2, (D, B)),
            Room(D, 2, (A, A)),
        ),
        Hallway(),
    ))
    print(energy)


@utils.part(cli)
def part_2():
    energy = get_best_path(State(
        0,
        (
            Room(A, 4, (C, D, D, D)),
            Room(B, 4, (C, B, C, B)),
            Room(C, 4, (D, A, B, B)),
            Room(D, 4, (A, C, A, A)),
        ),
        Hallway(),
    ))
    print(energy)
