import enum
import re

import click

import utils


class PasswordPolicyType(enum.Enum):
    FREQUENCY = 'FREQUENCY'
    POSITION = 'POSITION'


class PasswordPolicy:
    REGEX = r'(?P<x>\d+)-(?P<y>\d+) (?P<letter>[a-z])'

    def __init__(self, policy_type, letter, x, y):
        self.policy_type = policy_type
        self.letter = letter
        self.x = x
        self.y = y

    @staticmethod
    def parse(policy_type, string):
        match = re.match(PasswordPolicy.REGEX, string)
        if not match:
            raise ValueError(f'{string} is not a valid password policy')

        return PasswordPolicy(
            policy_type,
            match.group('letter'),
            int(match.group('x')),
            int(match.group('y')),
        )

    def is_valid(self, password):
        if self.policy_type == PasswordPolicyType.FREQUENCY:
            count = len([char for char in password if char == self.letter])
            return self.x <= count <= self.y

        return (password[self.x - 1] == self.letter) ^ (password[self.y - 1] == self.letter)


def get_valid_passwords(policy_type):
    passwords = utils.get_input(__file__, delimiter=': ', cast=str)
    valid_passwords = 0

    for policy_str, password in passwords:
        policy = PasswordPolicy.parse(policy_type, policy_str)
        valid_passwords += policy.is_valid(password)

    return valid_passwords


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    print(get_valid_passwords(PasswordPolicyType.FREQUENCY))


@cli.command()
def part_2():
    print(get_valid_passwords(PasswordPolicyType.POSITION))


if __name__ == '__main__':
    cli()
