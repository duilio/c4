import numpy as np

from c4.evaldiff import evaldiff
from c4.engine.base import Engine
from c4.evaluate import Evaluator, INF


class GreedyEngine(Engine):
    def __init__(self):
        self._evaluator = Evaluator()
        self.evaluate = self._evaluator.evaluate

    def choose(self, board):
        moves = board.moves()
        m = moves[0]
        moves = moves[1:]

        bestmove = m
        bestscore = -self.evaluate(board.move(m))

        for m in moves:
            score = -self.evaluate(board.move(m))
            if score > bestscore:
                bestmove = m
                bestscore = score

        print('Bestscore:', bestscore)
        return bestmove

    def __str__(self):
        return 'Greedy'


class WeightedGreedyEngine(Engine):
    """Same as GreedyEngine but move randomly using scores as weights

    """
    def __init__(self, verbose=True):
        self._evaluator = Evaluator()
        self._verbose = verbose
        self.evaluate = self._evaluator.evaluate

    def choose(self, board):
        moves = board.moves()

        # forced move?
        if len(moves) < 2:
            return moves[0]

        # winning move or threat blocking?
        scores = [evaldiff(board, m) for m in moves]
        if max(scores) >= INF - 1:
            return max(zip(scores, moves))[1]

        weights = np.array(scores, dtype=float) + 1

        if weights.sum() == 0:
            weights = np.array([1 / len(moves)] * len(moves), dtype=float)
        else:
            weights /= weights.sum()

        selected_move = np.random.choice(moves, p=weights)

        if self._verbose:
            selected_score = scores[list(moves).index(selected_move)]
            print('Selected move %d with score %s' % (selected_move,
                                                      selected_score))

        return selected_move

    def __str__(self):
        return 'Weighted Greedy'
