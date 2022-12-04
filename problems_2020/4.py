import functools
import re

import click
import marshmallow

from marshmallow import fields, validate
from marshmallow.exceptions import ValidationError

import utils


HEIGHT_REGEX = r'^(?P<value>\d+)(?P<unit>cm|in)$'
HAIR_COLOR_REGEX = r'^#[a-f0-9]{6}$'
PASSPORT_ID_REGEX = r'^\d{9}$'


def year_in_range(min_year, max_year, year):
    if not year.isnumeric():
        raise ValidationError('Not a valid year: must be a number')

    if not min_year <= int(year) <= max_year:
        raise ValidationError(f'Must be a year in the range [{min_year}, {max_year}]')


def valid_height(height):
    match = re.match(HEIGHT_REGEX, height)

    if not match:
        raise ValidationError(f'Not a valid height: must match {HEIGHT_REGEX}')

    unit = match.group('unit')
    value = int(match.group('value'))

    if unit == 'cm' and not 150 <= value <= 193:
        raise ValidationError('Height must be between 150cm and 193cm')

    if unit == 'in' and not 59 <= value <= 76:
        raise ValidationError('Height must be between 59in and 76in')


class PassportSchema(marshmallow.Schema):
    byr = fields.String(required=True, validate=functools.partial(year_in_range, 1920, 2002))
    iyr = fields.String(required=True, validate=functools.partial(year_in_range, 2010, 2020))
    eyr = fields.String(required=True, validate=functools.partial(year_in_range, 2020, 2030))
    hgt = fields.String(required=True, validate=valid_height)
    hcl = fields.String(required=True, validate=validate.Regexp(HAIR_COLOR_REGEX))
    ecl = fields.String(required=True, validate=validate.OneOf(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']))
    pid = fields.String(required=True, validate=validate.Regexp(PASSPORT_ID_REGEX))
    cid = fields.String()

    def __init__(self, *args, strict=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not strict:
            for field_name in self.fields:
                self.fields[field_name].validators = []


def is_valid_passport(line, strict):
    try:
        PassportSchema(strict=strict).load(dict(tuple(item.split(':')) for item in line))
        return True
    except marshmallow.ValidationError:
        return False


def get_valid_passports(strict=False):
    lines = utils.get_input(
        __file__,
        line_delimiter='\n\n',
        delimiter=[' ', '\n'],
        cast=str,
    )
    return [is_valid_passport(line, strict) for line in lines].count(True)


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    print(get_valid_passports())


@utils.part(cli)
def part_2():
    print(get_valid_passports(strict=True))


if __name__ == '__main__':
    cli()
