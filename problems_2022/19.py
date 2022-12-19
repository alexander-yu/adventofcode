import collections
import math

import parse

import utils


def get_blueprints():
    return utils.get_input(
        cast=lambda line: parse.parse(
            'Blueprint {:d}: '
            'Each ore robot costs {:d} ore. '
            'Each clay robot costs {:d} ore. '
            'Each obsidian robot costs {:d} ore and {:d} clay. '
            'Each geode robot costs {:d} ore and {:d} obsidian.',
            line,
        ),
        delimiter=None,
        line_delimiter='\n',
    )


def get_max_geodes(blueprint, total_time):
    blueprint_id, o_o_cost, c_o_cost, ob_o_cost, ob_c_cost, g_o_cost, g_ob_cost = blueprint
    max_o_cost = max(o_o_cost, c_o_cost, ob_o_cost, g_o_cost)

    # State is structured as:
    # (ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode, remaining time)
    initial = (1, 0, 0, 0, 0, 0, 0, 0, total_time)

    queue = collections.deque([initial])
    seen = set()
    times = set()
    max_geodes = 0

    while queue:
        r_o, r_c, r_ob, r_g, o, c, ob, g, time = queue.popleft()

        if time not in times:
            times.add(time)
            print(f'[{blueprint_id}] Time left: {time:<2} | Queue size: {len(queue)}')

        max_geodes = max(max_geodes, g)

        if time == 0:
            continue

        # If we have more resources than we could possibly need, trim it down to reduce state space.
        # For example, note that for clay, if we have r_c clay robots and more than
        # ob_c_cost + (ob_c_cost - r_c) * (t - 1) clay, we can buy a obsidian robot next (which we are guaranteed
        # to be able to afford since we also make sure that r_c <= ob_c_cost, see below). Then for each
        # subsequent turn, if we conservatively assume we always buy another obsidian robot, after producing the next
        # batch of clay we have more than r_c + (ob_c_cost - r_c) * (t - 1) = (ob_c_cost - r_c) * (t - 2) + ob_c_cost,
        # so inductively we can keep affording to buy obsidian robots, and at the end we're still left over with clay.
        o = min(o, max_o_cost + (max_o_cost - r_o) * (time - 1))
        c = min(c, ob_c_cost + (ob_c_cost - r_c) * (time - 1))
        ob = min(ob, g_ob_cost + (g_ob_cost - r_ob) * (time - 1))

        state = (r_o, r_c, r_ob, r_g, o, c, ob, g, time)

        if state in seen:
            continue

        seen.add(state)

        # For ore, clay, and obsidian robots, don't make more than we would possibly need. Note that
        # we can only make robot per turn, so the number of robots we need for ore/clay/obsidian should
        # be no more than the max amount of each resource that we would need to consume to make a robot.
        if o >= o_o_cost and r_o < max_o_cost:
            queue.append((
                r_o + 1, r_c, r_ob, r_g, o - o_o_cost + r_o, c + r_c, ob + r_ob, g + r_g, time - 1
            ))
        if o >= c_o_cost and r_c < ob_c_cost:
            queue.append((
                r_o, r_c + 1, r_ob, r_g, o - c_o_cost + r_o, c + r_c, ob + r_ob, g + r_g, time - 1
            ))
        if o >= ob_o_cost and c >= ob_c_cost and r_ob < g_ob_cost:
            queue.append((
                r_o, r_c, r_ob + 1, r_g, o - ob_o_cost + r_o, c - ob_c_cost + r_c, ob + r_ob, g + r_g, time - 1
            ))
        if o >= g_o_cost and ob >= g_ob_cost:
            queue.append((
                r_o, r_c, r_ob, r_g + 1, o - g_o_cost + r_o, c + r_c, ob - g_ob_cost + r_ob, g + r_g, time - 1
            ))

        queue.append((
            r_o, r_c, r_ob, r_g, o + r_o, c + r_c, ob + r_ob, g + r_g, time - 1
        ))

    return max_geodes


@utils.part
def part_1():
    blueprints = get_blueprints()
    print(sum(blueprint[0] * get_max_geodes(blueprint, 24) for blueprint in blueprints))


@utils.part
def part_2():
    blueprints = get_blueprints()
    print(math.prod([get_max_geodes(blueprint, 32) for blueprint in blueprints[:3]]))
