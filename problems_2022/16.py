import collections
import itertools
import re

from boltons import iterutils

import utils


def get_data():
    matches = utils.get_input(
        cast=lambda line: re.match(
            r'Valve (?P<valve>.+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<next_valves>.+)',
            line,
        ),
        delimiter=None,
        line_delimiter='\n',
    )
    data = []

    for match in matches:
        data.append((
            match.group('valve'),
            int(match.group('rate')),
            match.group('next_valves').split(', '),
        ))

    neighbors = {}
    rates = {}
    valves_to_open = set()

    for valve, rate, valve_neighbors in data:
        neighbors[valve] = valve_neighbors
        rates[valve] = rate

        if rate:
            valves_to_open.add(valve)

    return neighbors, rates, frozenset(valves_to_open)


@utils.part
def part_1():
    neighbors, rates, _ = get_data()

    open_valves = set()
    seen = {}
    max_so_far = 0

    def search(time, me, pressure):
        nonlocal max_so_far

        if seen.get((time, me), -1) >= pressure:
            return

        seen[time, me] = pressure

        if time == 30:
            max_so_far = max(max_so_far, pressure)
            return

        net_pressure = sum(rates[valve] for valve in open_valves)

        if me not in open_valves and rates[me]:
            open_valves.add(me)
            search(time + 1, me, pressure + net_pressure + rates[me])
            open_valves.remove(me)

        for neighbor in neighbors[me]:
            search(time + 1, neighbor, pressure + net_pressure)

    search(1, 'AA', 0)
    print(max_so_far)


@utils.part
def part_2():
    neighbors, rates, valves_to_open = get_data()

    open_valves = set()
    visited = {}
    max_so_far = 0

    def search(time, me, elephant, pressure):
        nonlocal max_so_far

        if visited.get((time, me, elephant), -1) >= pressure:
            return

        visited[time, me, elephant] = pressure

        if time == 26:
            max_so_far = max(max_so_far, pressure)
            return

        pressure += sum(rates[valve] for valve in open_valves)

        # all open? just stay put...
        if len(open_valves) == len(valves_to_open):
            search(time + 1, me, elephant, pressure)
            return

        if me not in open_valves and rates[me]:
            open_valves.add(me)

            if elephant not in open_valves and rates[elephant]:
                open_valves.add(elephant)
                search(
                    time + 1,
                    me,
                    elephant,
                    pressure + rates[me] + rates[elephant]
                )
                open_valves.remove(elephant)

            for neighbor in neighbors[elephant]:
                search(
                    time + 1,
                    me,
                    neighbor,
                    pressure + rates[me]
                )

            open_valves.remove(me)

        for me_neighbor in neighbors[me]:
            if elephant not in open_valves and rates[elephant]:
                open_valves.add(elephant)
                search(
                    time + 1,
                    me_neighbor,
                    elephant,
                    pressure + rates[elephant]
                )
                open_valves.remove(elephant)

            for elephant_neighbor in neighbors[elephant]:
                search(
                    time + 1,
                    me_neighbor,
                    elephant_neighbor,
                    pressure,
                )

    search(1, 'AA', 'AA', 0)
    print(max_so_far)


@utils.part
def part_2_disjoint():
    neighbors, rates, valves_to_open = get_data()
    states = {}
    masks = {valve: 1 << i for i, valve in enumerate(valves_to_open)}

    def next_states(current_states):
        for me, open_valves, flow, pressure in current_states:
            candidate_states = []

            if me in masks and ~open_valves & masks[me]:
                candidate_states.append((me, open_valves | masks[me], flow + rates[me]))

            for neighbor in neighbors[me]:
                candidate_states.append((neighbor, open_valves, flow))

            for state in candidate_states:
                if state not in states or states[state] < pressure + flow:
                    states[state] = pressure + flow
                    yield (*state, pressure + flow)

    current_states = [('AA', 0, 0, 0)]

    for _ in range(26):
        current_states = list(next_states(current_states))

    grouped_states = collections.defaultdict(list)

    for state, pressure in states.items():
        open_valves = state[1]
        grouped_states[open_valves].append(pressure)

    best_states = {
        open_valves: max(pressures)
        for open_valves, pressures in grouped_states.items()
    }

    print(max(
        me_pressure + elephant_pressure
        for (me_open_valves, me_pressure), (elephant_open_valves, elephant_pressure)
        in itertools.combinations(best_states.items(), 2)
        if not me_open_valves & elephant_open_valves
    ))
