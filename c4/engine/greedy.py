import numpy as np

from c4.evaluate import Evaluator, INF
from c4.engine.base import Engine


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

        # winning move?
        scores = [-self.evaluate(board.move(m)) for m in moves]
        if max(scores) == INF:
            return sorted(zip(scores, moves), reverse=True)[0][1]

        scores = np.array(scores, dtype=float)
        weights = scores + (abs(scores.min()) + 1)

        if weights.sum() == 0:
            weights = np.array([1 / len(moves)] * len(moves), dtype=float)
        else:
            weights /= weights.sum()

        selected_move = np.random.choice(moves, p=weights)
        selected_score = scores[list(moves).index(selected_move)]

        if self._verbose:
            print('Selected move %d with score %s' % (selected_move,
                                                      selected_score))

        return selected_move

    def __str__(self):
        return 'Weighted Greedy'
