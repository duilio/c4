import numpy as np

from c4.board import Board
from c4.evaluate import INF

from c4.tables import evaldiff_lookup, evaldiff_threat_lookup


def evaldiff(board, m, weights=np.array([1, 3, 9, 27], dtype=int)):
    r = board.freerow(m)
    stm = board.stm
    indices = np.dot(Board.segments_around(board, r, m),
                     weights)
    partial_scores = evaldiff_lookup[stm][indices]

    if (partial_scores == 4**2).any():
        return INF

    if evaldiff_threat_lookup[stm][indices].any():
        return INF - 1

    return partial_scores.sum()
