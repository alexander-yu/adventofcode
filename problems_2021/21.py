import collections
import dataclasses
import functools
import itertools
import re

import utils


PLAYER_REGEX = r'Player \d starting position: (?P<position>\d+)'


class Die:
    def __init__(self):
        self.generator = itertools.cycle(range(1, 101))
        self.rolls = 0

    def roll(self):
        self.rolls += 3
        return sum(next(self.generator) for _ in range(3))


@dataclasses.dataclass(frozen=True)
class Player:
    position: int
    score: int = 0

    def move(self, value):
        position = self.position + value
        position = (position % 10) + 10 * (position % 10 == 0)
        score = self.score + position
        return Player(position, score=score)


@functools.cache
def quantum_wins(player_1, player_2, current_player):
    win_counts = collections.Counter()

    for rolls in itertools.product([1, 2, 3], repeat=3):
        roll = sum(rolls)

        players = {1: player_1, 2: player_2}
        player = players[current_player].move(roll)
        players[current_player] = player

        if player.score >= 21:
            win_counts[current_player] += 1
        else:
            next_player = 3 - current_player
            win_counts.update(quantum_wins(players[1], players[2], next_player))

    return win_counts


def get_players():
    players = utils.get_input(delimiter=None, cast=str)
    return [
        Player(int(re.match(PLAYER_REGEX, player).group('position')))
        for player in players
    ]


@utils.part
def part_1():
    player_1, player_2 = get_players()
    die = Die()

    while True:
        player_1 = player_1.move(die.roll())
        if player_1.score >= 1000:
            print(player_2.score * die.rolls)
            break

        player_2 = player_2.move(die.roll())
        if player_2.score >= 1000:
            print(player_1.score * die.rolls)
            break


@utils.part
def part_2():
    player_1, player_2 = get_players()
    win_counts = quantum_wins(player_1, player_2, 1)
    print(win_counts.most_common()[0][1])
