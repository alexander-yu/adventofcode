import collections
import itertools
import re

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

        # If all valves are open, just stay here
        if len(open_valves) == len(valves_to_open):
            search(time + 1, me, elephant, pressure)
            return

        # I could open the valve
        if me not in open_valves and rates[me]:
            open_valves.add(me)

            # Elephant could open the valve
            if elephant not in open_valves and rates[elephant]:
                open_valves.add(elephant)
                search(
                    time + 1,
                    me,
                    elephant,
                    pressure + rates[me] + rates[elephant]
                )
                open_valves.remove(elephant)

            # Elephant could just move
            for neighbor in neighbors[elephant]:
                search(
                    time + 1,
                    me,
                    neighbor,
                    pressure + rates[me]
                )

            open_valves.remove(me)

        # I could just move
        for me_neighbor in neighbors[me]:
            # Elephant could open the valve
            if elephant not in open_valves and rates[elephant]:
                open_valves.add(elephant)
                search(
                    time + 1,
                    me_neighbor,
                    elephant,
                    pressure + rates[elephant]
                )
                open_valves.remove(elephant)

            # Elephant could just move
            for elephant_neighbor in neighbors[elephant]:
                search(
                    time + 1,
                    me_neighbor,
                    elephant_neighbor,
                    pressure,
                )

    search(1, 'AA', 'AA', 0)
    print(max_so_far)


def bfs_search():
    neighbors, rates, valves_to_open = get_data()
    states = {}
    valves = {valve: 1 << i for i, valve in enumerate(valves_to_open)}

    def next_states(current_states):
        for me, open_valves, flow, pressure in current_states:
            candidate_states = []

            # If at a valve of interest and it's closed, open it
            if me in valves and ~open_valves & valves[me]:
                candidate_states.append((me, open_valves | valves[me], flow + rates[me]))

            # Alternatively, move to another valve
            for neighbor in neighbors[me]:
                candidate_states.append((neighbor, open_valves, flow))

            for state in candidate_states:
                if state not in states or states[state] < pressure + flow:
                    states[state] = pressure + flow
                    yield (*state, pressure + flow)

    current_states = [('AA', 0, 0, 0)]

    for _ in range(26):
        current_states = list(next_states(current_states))

    return states


@utils.part
def part_2_bfs_disjoint():
    """
    Somewhat of a more clever/simpler solution here than doing 2D DFS, where the idea is that you
    use BFS to compile a list of all possible 1-player states at the end of 26 minutes, with
    a bitset to represent open valves.

    Then you group them by the open valves at the end and select the state for maximal pressure
    for that given set of final open valves.

    Then, noting that you and the elephant operate on disjoint sets of open valves, we simply
    take all distinct pairs of final states with disjoint open valves and try to find the pair
    with maximal total pressure.
    """
    states = bfs_search()
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


def all_shortest_paths(adj):
    """Floyd-Warshall implementation"""
    valves = sorted(adj.keys())
    distances = {u: {v: float('inf') for v in valves} for u in valves}

    for u in valves:
        distances[u][u] = 0

        for v in adj[u]:
            distances[u][v] = 1

    for k, i, j in itertools.product(valves, repeat=3):
        if distances[i][j] > distances[i][k] + distances[k][j]:
            distances[i][j] = distances[i][k] + distances[k][j]

    return distances


def compressed_bfs_search():
    """
    This performs a BFS search on the possible 1-player states, but on a compressed weighted graph
    that whose nodes are only those with positive flow rates, and the edge weights represent
    the amount of time it takes to travel to the next valve and open it.
    """
    neighbors, rates, valves_to_open = get_data()
    masks = {valve: 1 << i for i, valve in enumerate(valves_to_open)}
    distances = all_shortest_paths(neighbors)

    # Compress the graph to only valves with a positive flow rate
    neighbors = {
        valve_1: [valve_2 for valve_2 in valves_to_open if valve_2 != valve_1]
        for valve_1 in valves_to_open
    }

    states = {}

    # Initialize queue with 1 valve already opened
    queue = collections.deque([
        (
            valve,
            masks[valve],
            # We store the total pressure that this opened valve will contribute for the entire 26 minutes instead
            # of just simulating each individual minute
            rates[valve] * (26 - distances['AA'][valve] - 1),
            distances['AA'][valve] + 1,
        )
        for valve in valves_to_open
    ])

    while queue:
        me, open_valves, pressure, time = queue.popleft()
        state = (me, open_valves)

        if state not in states or states[state] < pressure:
            states[state] = pressure

        for neighbor in neighbors[me]:
            # New time elapsed after traveling to the valve and opening it
            new_time = time + distances[me][neighbor] + 1

            # If valve is closed, we can get to it and open it, and we can get at least 1 minute of positive flow,
            # consider it a candidate next state
            if ~open_valves & masks[neighbor] and new_time < 26:
                new_state = (neighbor, open_valves | masks[neighbor])
                new_pressure = pressure + (26 - new_time) * rates[neighbor]

                if new_state not in states or states[new_state] < new_pressure:
                    states[new_state] = new_pressure
                    queue.append((*new_state, new_pressure, new_time))

    return states


@utils.part
def part_2_compressed_bfs_disjoint():
    """
    This is a variant on the other BFS disjoint solution, but instead we "compress" the graph.

    0-valves are completely useless and only serve as connection points to the actual valves that
    add pressure, so we can remove them entirely and form a new weighted graph using Floyd-Warshall
    to calculate the minimum distances between valves of interest.
    """
    states = compressed_bfs_search()
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
