import click

import utils


def get_loop(subject, key, mod):
    power = 1

    for i in range(mod):
        power *= subject
        power %= mod
        if power == key:
            return i + 1

    raise ValueError(
        f'Could not find loop size for subject {subject}, key {key}, and mod {mod}'
    )


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    card_key, door_key = utils.get_input(__file__, delimiter=None)
    subject, mod = 7, 20201227
    card_loop = get_loop(subject, card_key, mod)
    door_loop = get_loop(subject, door_key, mod)
    print(pow(subject, card_loop * door_loop, mod=mod))
