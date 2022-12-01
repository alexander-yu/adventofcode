import dataclasses

import click

import utils


@dataclasses.dataclass
class Fold:
    axis: str
    value: int


def fold_paper(dots, fold):
    new_dots = set()

    for x, y in dots:
        if fold.axis == 'x' and x > fold.value:
            new_dots.add((2 * fold.value - x, y))
        elif fold.axis == 'y' and y > fold.value:
            new_dots.add((x, 2 * fold.value - y))
        else:
            new_dots.add((x, y))

    return new_dots


def get_manual():
    dots, folds = utils.get_input(__file__, delimiter=None, line_delimiter='\n\n', cast=str)
    dots = set(tuple(dot) for dot in utils.parse(dots))
    folds = [
        Fold(axis, int(value))
        for axis, value in
        utils.parse(folds, delimiter='=', remove_prefix='fold along ', cast=str)
    ]
    return dots, folds


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    dots, folds = get_manual()
    dots = fold_paper(dots, folds[0])
    print(len(dots))


@cli.command()
@utils.part(__name__, 2)
def part_2():
    dots, folds = get_manual()

    for fold in folds:
        dots = fold_paper(dots, fold)

    max_x = max(dot[0] for dot in dots)
    max_y = max(dot[1] for dot in dots)

    for j in range(max_y + 1):
        for i in range(max_x + 1):
            point = (i, j)

            if point in dots:
                print('█', end='')
            else:
                print(' ', end='')

        print('\n')


if __name__ == '__main__':
    cli()
