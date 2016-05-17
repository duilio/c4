import numpy as np

from c4.board import Board
from c4.evaluate import INF


def evaldiff(board, m):
    r = board.freerow(m)

    stm = board.stm
    other = board.other

    threat = 0
    score = 0

    for s in Board.segments_around(board, r, m):
        c = np.bincount(s, minlength=3)
        c[0] -= 1
        c[stm] += 1

        if c[0] + c[stm] == 4:
            # add player advantages on this area
            if c[stm] == 4:
                return INF
            score += (c[stm] - 1) ** 2
        elif c[stm] == 1:
            # remove enemy advantages on this area
            score += c[other] ** 2

            # check if this is a threat, without this move the opponent has a
            # chance to win
            if c[0] == 0:
                threat = 1

    # let's give a very high score to blocked threats as it is almost like a
    # victory to block an opponent mate
    if threat:
        return INF - 1

    return score
