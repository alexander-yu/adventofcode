import math
import typing

from dataclasses import dataclass

import click

import utils


@dataclass
class Rule:
    field: str
    valid_ranges: typing.List[typing.Tuple[int, int]]

    def is_valid(self, number):
        return any(valid_range[0] <= number <= valid_range[1] for valid_range in self.valid_ranges)


def parse_rule(rule):
    field, valid_ranges = rule.split(': ')
    valid_ranges = [
        tuple(int(number) for number in valid_range.split('-'))
        for valid_range in valid_ranges.split(' or ')
    ]
    return Rule(field, valid_ranges)


def get_invalid_numbers(ticket, rules):
    invalid_numbers = []

    for number in ticket:
        if not any(rule.is_valid(number) for rule in rules):
            invalid_numbers.append(number)

    return invalid_numbers


def parse_notes():
    rules, my_ticket, nearby_tickets = utils.get_input(__file__, delimiter='\n', cast=str, line_delimiter='\n\n')

    rules = [parse_rule(rule) for rule in rules]
    my_ticket = [int(number) for number in my_ticket[1].split(',')]
    nearby_tickets = [
        [int(number) for number in nearby_ticket.split(',')]
        for nearby_ticket in nearby_tickets[1:]
    ]

    return rules, my_ticket, nearby_tickets


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    rules, _, nearby_tickets = parse_notes()
    error_rate = 0

    for nearby_ticket in nearby_tickets:
        error_rate += sum(get_invalid_numbers(nearby_ticket, rules))

    print(error_rate)


@cli.command()
def part_2():
    rules, my_ticket, nearby_tickets = parse_notes()
    field_candidates = {
        i: set(rule.field for rule in rules)
        for i, _ in enumerate(rules)
    }

    for nearby_ticket in nearby_tickets:
        if get_invalid_numbers(nearby_ticket, rules):
            continue

        # Discard any candidates that produce violations in valid tickets
        for i, number in enumerate(nearby_ticket):
            for rule in rules:
                if not rule.is_valid(number):
                    field_candidates[i].discard(rule.field)

    fields = {}
    sorted_field_candidates = sorted(field_candidates.items(), key=lambda x: len(x[1]), reverse=True)

    # In order for a unique solution to exist, after the discarding round above, there must be a field
    # with exactly one candidate. Moreover, each time we eliminate that candidate from the other candidate
    # sets, there must then be another field with exactly one candidate, etc., until all fields have been
    # solved.
    while sorted_field_candidates:
        i, candidates = sorted_field_candidates.pop()

        assert len(candidates) == 1
        assert i not in fields

        field = candidates.pop()
        fields[i] = field
        for _, field_candidates in sorted_field_candidates:
            field_candidates.discard(field)

    print(
        math.prod(
            my_ticket[i]
            for i, field in fields.items()
            if field.startswith('departure')
        )
    )



if __name__ == '__main__':
    cli()
