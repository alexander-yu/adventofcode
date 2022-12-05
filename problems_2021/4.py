import collections

import click

import utils


class Board:
    def __init__(self, board, dim):
        self.board = board
        self.marked = set()
        self.marked_rows = collections.Counter()
        self.marked_columns = collections.Counter()
        self.dim = dim

    @staticmethod
    def parse(board_str):
        board = {}
        dim = 0

        for i, row in enumerate(board_str.split('\n')):
            dim += 1
            for j, val in enumerate(row.strip().split()):
                val = int(val.strip())
                board[val] = (i, j)

        return Board(board, dim)

    def mark(self, number):
        coord = self.board.get(number)

        if coord:
            self.marked.add(coord)
            self.marked_rows.update([coord[0]])
            self.marked_columns.update([coord[1]])

    def is_won(self):
        if self.marked_rows and self.marked_rows.most_common(1)[0][1] == self.dim:
            return True
        if self.marked_columns and self.marked_columns.most_common(1)[0][1] == self.dim:
            return True
        return False

    def unmarked_sum(self):
        return sum(
            number
            for number, coord in self.board.items()
            if coord not in self.marked
        )


def get_initial_state():
    lines = utils.get_input(__file__, delimiter=None, cast=str, line_delimiter='\n\n')
    numbers = [int(val) for val in lines[0].split(',')]
    return numbers, [Board.parse(board) for board in lines[1:]]


@click.group()
def cli():
    pass


@utils.part(cli)
def part_1():
    numbers, boards = get_initial_state()

    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.is_won():
                print(board.unmarked_sum() * number)
                return


@utils.part(cli)
def part_2():
    numbers, boards = get_initial_state()
    won_boards = []

    for number in numbers:
        remaining_boards = []

        for board in boards:
            board.mark(number)

            if board.is_won():
                won_boards.append((board, number))
            else:
                remaining_boards.append(board)

        boards = remaining_boards

    board, number = won_boards[-1]
    print(board.unmarked_sum() * number)
