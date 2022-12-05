import copy
import enum

from dataclasses import dataclass

import click

import utils


class InfiniteLoopException(Exception):
    def __init__(self, program):
        super().__init__('Infinite loop detected')
        self.program = program


class InstructionType(enum.Enum):
    NOOP = 'nop'
    ACCUMULATOR = 'acc'
    JUMP = 'jmp'


@dataclass
class Instruction:
    type: InstructionType
    arg: int


class Program:
    def __init__(self, instructions):
        self.accumulator = 0
        self.instructions = instructions
        self.seen_instructions = set()
        self.position = 0
        self.handlers = {
            InstructionType.NOOP: self._noop,
            InstructionType.ACCUMULATOR: self._add_to_accumulator,
            InstructionType.JUMP: self._jump,
        }

    def _noop(self, _):
        self.position += 1

    def _add_to_accumulator(self, arg):
        self.accumulator += arg
        self.position += 1

    def _jump(self, arg):
        self.position += arg

    def run_next(self):
        if self.position in self.seen_instructions:
            raise InfiniteLoopException(self)

        self.seen_instructions.add(self.position)

        instruction = self.instructions[self.position]
        handler = self.handlers[instruction.type]
        handler(instruction.arg)

    def run(self):
        while len(self.instructions) - 1 not in self.seen_instructions:
            self.run_next()


def get_instructions():
    return [
        Instruction(InstructionType(instruction_type), int(arg))
        for instruction_type, arg in utils.get_input(__file__, delimiter=' ', cast=str)
    ]


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    program = Program(get_instructions())
    try:
        program.run()
    except InfiniteLoopException as exc:
        print(exc.program.accumulator)


@utils.part(cli)
def part_2():
    instructions = get_instructions()

    for i, _ in enumerate(instructions):
        instructions = copy.deepcopy(get_instructions())
        instruction = instructions[i]

        if instruction.type == InstructionType.NOOP:
            instruction.type = InstructionType.JUMP
        elif instruction.type == InstructionType.JUMP:
            instruction.type = InstructionType.NOOP
        else:
            continue

        program = Program(instructions)

        try:
            program.run()
        except InfiniteLoopException:
            continue
        else:
            print(program.accumulator)
            return
