import numpy as np

from c4.board import Board, PLAYER1, PLAYER2


class Evaluator(object):
    def __init__(self, weights=[0, 0, 1, 4, 0]):
        self._weights = np.asarray(weights)

    def evaluate(self, board):
        scores = {PLAYER1: [0]*5,
                  PLAYER2: [0]*5}

        for s in Board.segments(board):
            z = (s == 0).sum()
            for p in (PLAYER1, PLAYER2):
                c = (s == p).sum()
                if c + z == 4:
                    scores[p][c] += 1

        scores[PLAYER1] = (self._weights * scores[PLAYER1]).sum()
        scores[PLAYER2] = (self._weights * scores[PLAYER2]).sum()

        score = scores[PLAYER1] - scores[PLAYER2]
        if board.stm == PLAYER1:
            return score
        else:
            return -score
