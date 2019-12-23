import itertools

import click

import utils

from problems_2019 import intcode


def get_computer(i):
    memory = utils.get_input(__file__, test=False)[0]
    program = intcode.Program(memory, initial_inputs=[i], output_mode=intcode.OutputMode.PIPE)
    return program


def run(computers, return_first_nat_y=False):
    nat = None
    last_y = None
    no_packets = 0

    while True:
        packets_sent = False
        for computer in computers:
            address, return_signal = computer.run()
            if return_signal == intcode.ReturnSignal.AWAITING_INPUT:
                computer.add_inputs(-1)
                continue

            packets_sent = True

            x = computer.run_until_wait()
            y = computer.run_until_wait()

            if address == 255:
                nat = (x, y)

                if return_first_nat_y:
                    return y

                continue

            computers[address].add_inputs(x, y)

        if not packets_sent:
            no_packets += 1

        if no_packets >= 2:
            no_packets = 0
            computers[0].add_inputs(*nat)

            if nat[1] == last_y:
                return last_y

            last_y = nat[1]


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    computers = [get_computer(i) for i in range(50)]
    run(computers)


@cli.command()
def part_2():
    computers = [get_computer(i) for i in range(50)]
    run(computers)


if __name__ == '__main__':
    cli()
