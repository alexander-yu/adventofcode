import itertools

import utils

from problems_2019 import intcode


def run_thrusters(memory, phase_settings, loop):
    programs = [
        intcode.Program(memory[:], initial_inputs=[phase_setting], output_mode=intcode.OutputMode.PIPE)
        for phase_setting in phase_settings
    ]
    signal = 0
    halt_loop = False

    while not halt_loop:
        for program in programs:
            signal, exit_signal = program.run(signal)
            halt_loop = exit_signal == intcode.ReturnSignal.RETURN_AND_HALT

        if not loop:
            break

    return signal


@utils.part
def part_1():
    memory = utils.get_input()[0]
    print(max(
        run_thrusters(memory, phase_settings, False)
        for phase_settings
        in itertools.permutations(range(0, 5))
    ))


@utils.part
def part_2():
    memory = utils.get_input()[0]
    print(max(
        run_thrusters(memory, phase_settings, True)
        for phase_settings
        in itertools.permutations(range(5, 10))
    ))
