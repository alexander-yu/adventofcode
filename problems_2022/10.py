import dataclasses

import utils


CHECKPOINTS = [20, 60, 100, 140, 180, 220]


@dataclasses.dataclass
class State:
    register: int = 1
    cycles: int = 0
    screen: str = ''
    checkpoint_signals: list = dataclasses.field(default_factory=list)

    def render(self):
        if abs(self.register - self.cycles % 40) <= 1:
            self.screen += '#'
        else:
            self.screen += ' '

        if self.cycles % 40 == 39:
            self.screen += '\n'

    def tick(self, n: int = 1):
        for _ in range(n):
            self.render()
            self.cycles += 1

            if self.cycles in CHECKPOINTS:
                self.checkpoint_signals.append(self.cycles * self.register)


def execute_instructions():
    instructions = utils.get_input(__file__, cast=str, delimiter=' ', line_delimiter='\n')
    state = State()

    for instruction in instructions:
        if instruction[0] == 'noop':
            state.tick()
        else:
            value = int(instruction[1])
            state.tick(n=2)
            state.register += value

    return state


@utils.part
def part_1():
    state = execute_instructions()
    print(sum(state.checkpoint_signals))


@utils.part
def part_2():
    state = execute_instructions()
    print(state.screen)
