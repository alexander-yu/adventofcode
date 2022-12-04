import collections
import itertools

import click

import utils


def get_decks():
    decks = utils.get_input(__file__, cast=str, delimiter='\n', line_delimiter='\n\n')
    decks = [[int(card) for card in deck[1:]] for deck in decks]
    return [collections.deque(deck) for deck in decks]


def play_round(decks, recursive=False):
    cards = [deck.popleft() for deck in decks]
    winner = None

    if recursive:
        if all(len(deck) >= card for deck, card in zip(decks, cards)):
            winner = play(
                [
                    collections.deque(itertools.islice(deck, card))
                    for deck, card in zip(decks, cards)
                ],
                recursive=True,
            )

    if winner is None:
        winner = cards.index(max(cards))

    return winner, [cards[winner]] + [card for i, card in enumerate(cards) if i != winner]


def get_state(decks):
    return tuple(tuple(deck) for deck in decks)


def play(decks, recursive=False):
    previous_rounds = set()
    winner = None

    while all(decks):
        if recursive:
            state = get_state(decks)
            if state in previous_rounds:
                return 0
            previous_rounds.add(state)

        winner, cards = play_round(decks, recursive=recursive)
        decks[winner].extend(cards)

    return winner


def get_score(deck):
    return sum((len(deck) - i) * card for i, card in enumerate(deck))


@click.group()
def cli():
    pass


@cli.command
@utils.part
def part_1():
    decks = get_decks()
    winner = play(decks)
    print(get_score(decks[winner]))


@cli.command
@utils.part
def part_2():
    decks = get_decks()
    winner = play(decks, recursive=True)
    print(get_score(decks[winner]))


if __name__ == '__main__':
    cli()
