import collections
import enum
import inspect


class ArgMode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class ArgType(enum.Enum):
    READ = 0
    WRITE = 1


class ReturnSignal(enum.Enum):
    NONE = 0
    JUMPED = 1
    RETURN_AND_WAIT = 2
    RETURN_AND_HALT = 3
    AWAITING_INPUT = 4


class OutputMode(enum.Enum):
    PRINT = 0
    PIPE = 1
    BUFFER = 2


BINOP_ARG_TYPES = (ArgType.READ, ArgType.READ, ArgType.WRITE)
JUMP_ARG_TYPES = (ArgType.READ, ArgType.READ)
EXIT_SIGNALS = frozenset([
    ReturnSignal.RETURN_AND_HALT,
    ReturnSignal.RETURN_AND_WAIT,
    ReturnSignal.AWAITING_INPUT,
])


def commands_to_input(commands):
    return [
        ord(ch)
        for ch in
        ''.join(command + '\n' for command in commands)
    ]


class Instruction:
    def __init__(self, method, arg_types):
        self.method = method
        self.arg_types = arg_types
        assert len(self.arg_types) == len(inspect.signature(self.method).parameters)


class Memory:
    def __init__(self, memory):
        self.memory = collections.defaultdict(int)

        if isinstance(memory, list):
            self.memory.update({i: val for i, val in enumerate(memory)})
        elif isinstance(memory, dict):
            self.memory.update(memory)
        else:
            raise Exception(f'Expected list or dict, got {type(memory)}')

    def __getitem__(self, i):
        if i < 0:
            raise IndexError
        return self.memory[i]

    def __setitem__(self, i, val):
        if i < 0:
            raise IndexError
        self.memory[i] = val


class Program:
    def __init__(self, memory, initial_inputs=None, output_mode=OutputMode.PRINT):
        self.memory = Memory(memory)
        self.pointer = 0
        self.inputs = collections.deque(initial_inputs or [])
        self.outputs = collections.deque()
        self.output_mode = output_mode
        self.relative_base = 0
        self.instructions = {
            1: Instruction(
                lambda arg_1, arg_2, pos: self.write(pos, arg_1 + arg_2),
                BINOP_ARG_TYPES,
            ),
            2: Instruction(
                lambda arg_1, arg_2, pos: self.write(pos, arg_1 * arg_2),
                BINOP_ARG_TYPES,
            ),
            3: Instruction(
                self.input,
                [ArgType.WRITE],
            ),
            4: Instruction(
                self.output,
                [ArgType.READ],
            ),
            5: Instruction(
                lambda arg, pos: self.jump(arg != 0, pos),
                JUMP_ARG_TYPES,
            ),
            6: Instruction(
                lambda arg, pos: self.jump(arg == 0, pos),
                JUMP_ARG_TYPES,
            ),
            7: Instruction(
                lambda arg_1, arg_2, pos: self.write(pos, int(arg_1 < arg_2)),
                BINOP_ARG_TYPES,
            ),
            8: Instruction(
                lambda arg_1, arg_2, pos: self.write(pos, int(arg_1 == arg_2)),
                BINOP_ARG_TYPES,
            ),
            9: Instruction(
                self.adjust_relative_base,
                [ArgType.READ],
            ),
            99: Instruction(
                lambda: ReturnSignal.RETURN_AND_HALT,
                [],
            )
        }

    def write(self, pointer, val):
        self.memory[pointer] = val
        return ReturnSignal.NONE

    def input(self, pointer):
        if self.inputs:
            return self.write(pointer, self.inputs.popleft())
        return ReturnSignal.AWAITING_INPUT

    def output(self, val):
        self.outputs.append(val)

        if self.output_mode == OutputMode.PIPE:
            return ReturnSignal.RETURN_AND_WAIT

        if self.output_mode == OutputMode.PRINT:
            print(val)

        return ReturnSignal.NONE

    def jump(self, condition, pointer):
        if condition:
            self.pointer = pointer
            return ReturnSignal.JUMPED
        return ReturnSignal.NONE

    def adjust_relative_base(self, val):
        self.relative_base += val
        return ReturnSignal.NONE

    def get_next_instruction(self):
        instruction_code = '{:0>5d}'.format(self.memory[self.pointer])
        opcode = int(instruction_code[-2:])
        arg_modes = [ArgMode(int(x)) for x in list(instruction_code[-3::-1])]
        return self.instructions[opcode], arg_modes

    def get_arg(self, pointer, arg_type, arg_mode):
        arg = self.memory[pointer]

        if arg_mode == ArgMode.RELATIVE:
            arg += self.relative_base
        elif arg_mode == ArgMode.IMMEDIATE:
            return arg

        if arg_type == ArgType.READ:
            return self.memory[arg]
        else:
            return arg

    def run_instruction(self, instruction, arg_modes):
        args = [
            self.get_arg(self.pointer + i + 1, arg_type, arg_mode)
            for i, (arg_type, arg_mode) in enumerate(zip(instruction.arg_types, arg_modes))
        ]
        return instruction.method(*args)

    def add_inputs(self, *inputs):
        self.inputs.extend(inputs)

    def yield_outputs(self, stop_when_finished=True):
        while self.outputs:
            yield self.outputs.popleft()

        if not stop_when_finished:
            while True:
                yield None

    def copy(self):
        program = Program(self.memory.memory.copy())
        program.pointer = self.pointer
        program.inputs = self.inputs.copy()
        program.outputs = self.outputs.copy()
        program.output_mode = self.output_mode
        program.relative_base = self.relative_base
        return program

    def run(self, *inputs):
        self.add_inputs(*inputs)
        while True:
            instruction, arg_modes = self.get_next_instruction()
            return_signal = self.run_instruction(instruction, arg_modes)

            if return_signal not in [ReturnSignal.JUMPED, ReturnSignal.AWAITING_INPUT]:
                self.pointer += len(instruction.arg_types) + 1

            if return_signal in EXIT_SIGNALS:
                last_output = self.outputs[-1] if self.outputs else None
                return last_output, return_signal

    def run_until_halt(self, *inputs):
        output, return_signal = self.run(*inputs)
        assert return_signal == ReturnSignal.RETURN_AND_HALT
        return output

    def run_until_wait(self, *inputs):
        output, return_signal = self.run(*inputs)
        assert return_signal == ReturnSignal.RETURN_AND_WAIT
        return output
