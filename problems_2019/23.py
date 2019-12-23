import itertools

import click

import utils

from problems_2019 import intcode


def get_computer(i):
    memory = utils.get_input(__file__)[0]
    # Bootstrap computers with initial input of -1, since no packets
    # are received prior to the first round
    program = intcode.Program(memory, initial_inputs=[i, -1], output_mode=intcode.OutputMode.BUFFER)
    return program


def run(computers, return_first_nat=False):
    nat = None
    last_sent_nat = None

    while True:
        packets_sent = False
        for computer in computers:
            _, return_signal = computer.run()
            if return_signal == intcode.ReturnSignal.AWAITING_INPUT:
                computer.add_inputs(-1)
            if not computer.outputs:
                continue

            packets_sent = True
            address, x, y = itertools.islice(computer.yield_outputs(), 3)

            if address == 255:
                nat = (x, y)

                if return_first_nat:
                    return nat

                continue

            computers[address].add_inputs(x, y)

        if not packets_sent:
            computers[0].add_inputs(*nat)

            if last_sent_nat and nat[1] == last_sent_nat[1]:
                return last_sent_nat

            last_sent_nat = nat


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    computers = [get_computer(i) for i in range(50)]
    print(run(computers, return_first_nat=True)[1])


@cli.command()
def part_2():
    computers = [get_computer(i) for i in range(50)]
    print(run(computers)[1])


if __name__ == '__main__':
    cli()
