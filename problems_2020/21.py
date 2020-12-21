import collections
import itertools
import typing

from dataclasses import dataclass

import click

from boltons import iterutils

import utils


@dataclass
class Food:
    ingredients: typing.Set[str]
    allergens: typing.Set[str]

    @staticmethod
    def parse(ingredients_str, allergens_str):
        return Food(set(ingredients_str.split(' ')), set(allergens_str.split(', ')))


def get_foods():
    return [
        Food.parse(*food)
        for food in utils.get_input(
            __file__,
            delimiter=' (contains ',
            cast=str,
            rstrip=')',
        )
    ]


def get_hypoallergenic_ingredients(foods):
    ingredients = set(itertools.chain.from_iterable(food.ingredients for food in foods))
    allergens = set(itertools.chain.from_iterable(food.allergens for food in foods))
    hypoallergenic = set()

    for ingredient in ingredients:
        potentially_allergen = False

        for allergen in allergens:
            if all(ingredient in food.ingredients for food in foods if allergen in food.allergens):
                potentially_allergen = True
                break

        if not potentially_allergen:
            hypoallergenic.add(ingredient)

    return hypoallergenic


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    foods = get_foods()
    hypoallergenic = get_hypoallergenic_ingredients(foods)
    hypoallergenic_occurrences = len(list(itertools.chain.from_iterable(
        [ingredient for ingredient in food.ingredients if ingredient in hypoallergenic]
        for food in foods
    )))
    print(hypoallergenic_occurrences)


@cli.command()
def part_2():
    foods = get_foods()
    hypoallergenic = get_hypoallergenic_ingredients(foods)
    allergen_candidates = collections.defaultdict(set)

    for food in foods:
        for ingredient, allergen in itertools.product(food.ingredients, food.allergens):
            if ingredient not in hypoallergenic:
                allergen_candidates[allergen].add(ingredient)

    # Remove invalid candidates
    for allergen, ingredients in allergen_candidates.items():
        for ingredient in list(ingredients):
            if not all(ingredient in food.ingredients for food in foods if allergen in food.allergens):
                ingredients.remove(ingredient)

    allergen_map = {}

    while allergen_candidates:
        # Find the next allergen that has been solved, i.e. only 1 candidate left
        solved_allergen = iterutils.first(
            allergen_candidates,
            key=lambda allergen: len(allergen_candidates[allergen]) == 1,
        )
        ingredient = allergen_candidates[solved_allergen].pop()
        allergen_map[solved_allergen] = ingredient

        # Remove allergen from candidate map and remove ingredient from other candidate lists
        del allergen_candidates[solved_allergen]
        for allergen, ingredients in allergen_candidates.items():
            ingredients.discard(ingredient)

    allergens = sorted(allergen_map.keys())
    print(','.join(allergen_map[allergen] for allergen in allergens))


if __name__ == '__main__':
    cli()
