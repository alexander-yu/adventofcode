import enum
import itertools

import utils

from problems_2019 import intcode


DISPLAY_WIDTH = 37
DISPLAY_HEIGHT = 26
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


TILE_DISPLAYS = {
    TileID.EMPTY: ' ',
    TileID.WALL: '#',
    TileID.BLOCK: 'X',
    TileID.PADDLE: '-',
    TileID.BALL: '*',
}


class Game:
    def __init__(self, program):
        self.score = 0
        self.tiles = {}
        self.ball = None
        self.paddle = None
        self.program = program

    def display(self):
        for y in range(DISPLAY_HEIGHT):
            for x in range(DISPLAY_WIDTH):
                tile = self.tiles.get((x, y), TileID.EMPTY)
                print(TILE_DISPLAYS[tile], end='')
            print()

    def play(self, quarters=0):
        if quarters:
            self.program.memory[0] = quarters

        _, return_signal = self.program.run()

        while return_signal != intcode.ReturnSignal.RETURN_AND_HALT or self.program.outputs:
            x, y, output = itertools.islice(self.program.yield_outputs(stop_when_finished=False), 3)

            if (x, y) == SCORE_FLAG:
                self.score = output
            elif (x, y) != (None, None):
                tile_id = TileID(output)
                self.tiles[(x, y)] = tile_id

                if tile_id == TileID.PADDLE:
                    self.paddle = (x, y)
                elif tile_id == TileID.BALL:
                    self.ball = (x, y)
            else:
                assert return_signal == intcode.ReturnSignal.AWAITING_INPUT

                if self.ball[0] < self.paddle[0]:
                    joystick_input = Input.LEFT.value
                elif self.ball[0] > self.paddle[0]:
                    joystick_input = Input.RIGHT.value
                else:
                    joystick_input = Input.NEUTRAL.value

                _, return_signal = self.program.run(joystick_input)


def play(quarters=0):
    memory = utils.get_input(__file__)[0]
    program = intcode.Program(memory, output_mode=intcode.OutputMode.BUFFER)
    game = Game(program)
    game.play(quarters=quarters)
    return game


@utils.part
def part_1():
    game = play()
    print(len([tile_id for tile_id in game.tiles.values() if tile_id == TileID.BLOCK]))


@utils.part
def part_2():
    game = play(quarters=2)
    print(game.score)
