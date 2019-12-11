import functools

import click
import numpy as np

import utils


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    image = np.array(utils.get_input(__file__, delimiter='')[0]).reshape((-1, 6, 25))
    layer = min(image, key=lambda layer: np.sum(layer == 0))

    ones = np.sum(layer == 1)
    twos = np.sum(layer == 2)

    print(ones * twos)


@cli.command()
def part_2():
    image = np.array(utils.get_input(__file__, delimiter='')[0]).reshape((-1, 6, 25))
    decode = np.vectorize(lambda a, b: a if a != 2 else b)
    decoded_image = functools.reduce(decode, image)

    display = np.vectorize(lambda a: '#' if a == 0 else '.')
    for layer in display(decoded_image):
        print(''.join(layer))


if __name__ == '__main__':
    cli()
