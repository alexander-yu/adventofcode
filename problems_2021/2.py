import click

import utils


class Position:
    def __init__(self, version: int):
        self.version_handler = {
            1: self._run_instruction_v1,
            2: self._run_instruction_v2,
        }[version]

        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0

    def run_instruction(self, command: str, value: int):
        self.version_handler(command, value)

    def _run_instruction_v1(self, command: str, value: int):
        if command == 'forward':
            self.horizontal_position += value
        elif command == 'up':
            self.depth -= value
        elif command == 'down':
            self.depth += value
        else:
            raise ValueError(f'Unsupported command {command}')

    def _run_instruction_v2(self, command: str, value: int):
        if command == 'forward':
            self.horizontal_position += value
            self.depth += self.aim * value
        elif command == 'up':
            self.aim -= value
        elif command == 'down':
            self.aim += value
        else:
            raise ValueError(f'Unsupported command {command}')


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    instructions = utils.get_input(__file__, delimiter=' ', cast=str)
    position = Position(1)

    for command, value in instructions:
        position.run_instruction(command, int(value))

    print(position.horizontal_position * position.depth)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    instructions = utils.get_input(__file__, delimiter=' ', cast=str)
    position = Position(2)

    for command, value in instructions:
        position.run_instruction(command, int(value))

    print(position.horizontal_position * position.depth)


if __name__ == '__main__':
    cli()
