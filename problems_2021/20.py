from scipy import signal

import click
import numpy as np

import utils


KERNEL = np.reshape(2 ** np.arange(9), (3, 3))


def get_void(enhancement, iteration):
    if iteration == 0 or enhancement[0] == '.':
        return 0
    if enhancement[-1] == '#':
        return 1
    return iteration % 2


def enhance_image(iterations):
    enhancement, image = utils.get_input(__file__, delimiter=None, line_delimiter='\n\n', cast=str)
    image = utils.parse(image, delimiter='', cast=lambda pixel: int(pixel == '#'))
    light = [i for i, ch in enumerate(enhancement) if ch == '#']

    for i in range(iterations):
        image = signal.convolve2d(image, KERNEL, fillvalue=get_void(enhancement, i))
        image = np.isin(image, light).astype(int)

    return image


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    image = enhance_image(2)
    print(image.sum())


@utils.part(cli)
def part_2():
    image = enhance_image(50)
    print(image.sum())


if __name__ == '__main__':
    cli()
