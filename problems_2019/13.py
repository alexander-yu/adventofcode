import enum

import click

import utils

from problems_2019 import intcode


SCORE_FLAG = (-1, 0)


class TileID(enum.Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Input(enum.Enum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


def display(tiles):
    sym = {
        TileID.EMPTY: ' ',
        TileID.WALL: '#',
        TileID.BLOCK: 'X',
        TileID.PADDLE: '-',
        TileID.BALL: '*',
    }
    for y in range(37):
        for x in range(50):
            if (x, y) in tiles:
                tile = tiles[(x, y)]
            else:
                tile = TileID.EMPTY
            print(sym[tile]*2, end='')
        print()


class GameState:
    def __init__(self):
        self.score = 0
        self.tiles = {}
        self.ball = None
        self.paddle = None


class Game:
    def __init__(self, program):
        self.state = GameState()
        self.program = program
        self.program.output_mode = intcode.OutputMode.BUFFER

    def get_next_state(self, joystick_input):
        while True:
            _, return_signal = self.program.run()
            print(return_signal)
            if return_signal == intcode.ReturnSignal.RETURN_AND_HALT:
                break

            x = self.program.outputs.popleft()
            y = self.program.outputs.popleft()
            output = self.program.outputs.popleft()
            print('output', x, y, output)

            if (x, y) == SCORE_FLAG:
                self.state.score = output
                print('SCORE', output)
            else:
                tile_id = TileID(output)
                self.state.tiles[(x, y)] = tile_id

                if tile_id == TileID.PADDLE:
                    self.state.paddle = (x, y)
                    print('PADDLE', (x, y))
                elif tile_id == TileID.BALL:
                    self.state.ball = (x, y)
                    print('BALL', (x, y))

                    if self.state.ball[0] < self.state.paddle[0]:
                        joystick_input = Input.LEFT.value
                    elif self.state.ball[0] > self.state.paddle[0]:
                        joystick_input = Input.RIGHT.value
                    else:
                        joystick_input = Input.NEUTRAL.value

            print('blocks', len([tile_id for tile_id in self.state.tiles.values() if tile_id == TileID.BLOCK]))
            display(self.state.tiles)


def play(quarters=0):
    memory = utils.get_input(__file__)[0]

    if quarters:
        memory[0] = quarters

    program = intcode.Program(memory, initial_inputs=[Input.NEUTRAL.value], output_mode=intcode.OutputMode.PIPE)
    game = Game(program)

    joystick_input = Input.RIGHT.value

    game.get_next_state(joystick_input)

    return game.state.tiles, game.state.score


@click.group()
def cli():
    pass


@cli.command()
def part_1():
    tiles, _ = play()
    print(len([tile_id for tile_id in tiles.values() if tile_id == TileID.BLOCK]))
    print(tiles)


@cli.command()
def part_2():
    tiles, score = play(quarters=2)
    print(score)


if __name__ == '__main__':
    cli()
