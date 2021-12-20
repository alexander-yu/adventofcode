from scipy import signal

import click
import numpy as np

import utils


KERNEL = np.reshape(2 ** np.arange(9), (3, 3))


def enhance_image(iters):
    enhancement, image = utils.get_input(__file__, delimiter=None, line_delimiter='\n\n', cast=str)
    image = utils.parse(image, delimiter='', cast=lambda pixel: int(pixel == '#'))
    light = [i for i, ch in enumerate(enhancement) if ch == '#']

    for i in range(iters):
        image = signal.convolve2d(image, KERNEL, fillvalue=i % 2)
        image = np.isin(image, light).astype(int)

    return image


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    image = enhance_image(2)
    print(image.sum())


@cli.command()
@utils.part(__name__, 2)
def part_2():
    image = enhance_image(50)
    print(image.sum())


if __name__ == '__main__':
    cli()
