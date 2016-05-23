"""Winning moves book"""

import numpy as np

from c4.board import Board, PLAYER1, PLAYER2


WIN = 1
LOSS = -1
DRAW = 0
MAPPING = {
    'x': PLAYER1,
    'o': PLAYER2,
    'b': 0
}


class InvalidFormat(ValueError):
    pass


class Book(object):
    def __init__(self, filename):
        self._data = self.load_data(filename)

    def load_data(self, filename):
        data = {}

        with open(filename, 'r') as fin:
            for i, line in enumerate(fin):
                fields = line.rstrip().split(',')
                result = self.parse_result(fields[-1])
                board = self.parse_board(fields[:-1])

                key, _ = board.hashkey()
                if key in data:
                    continue

                data[key] = result

        print('Load %d positions' % len(data))
        return data

    def parse_result(self, result):
        if result == 'win':
            return WIN
        elif result == 'loss':
            return LOSS
        elif result == 'draw':
            return DRAW
        else:
            raise InvalidFormat()

    def parse_board(self, squares, mapping=MAPPING):
        squares = [mapping[x] for x in squares]
        pos = np.array(squares, dtype=int).reshape((7, 6))
        board = Board(pos, stm=PLAYER1, end=None)
        return board

    def __getitem__(self, board):
        return self._data.get(board.hashkey()[0], None)
