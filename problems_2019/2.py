import utils

from problems_2019 import intcode


def run_program(noun, verb):
    memory = utils.get_input()[0]
    memory[1] = noun
    memory[2] = verb
    program = intcode.Program(memory)
    program.run()
    return program.memory[0]


@utils.part
def part_1():
    print(run_program(12, 2))


@utils.part
def part_2():
    for noun in range(100):
        for verb in range(100):
            if run_program(noun, verb) == 19690720:
                print(100 * noun + verb)
                break
