import random
from functools import partial

from c4.evaluate import Evaluator
from c4.evaldiff import evaldiff


class MoveOrder(object):
    def __init__(self, name):
        if name == 'seq':
            self._order = self._order_seq
        elif name == 'random':
            self._order = self._order_random
        elif name == 'eval':
            self._order = self._order_eval
        elif name == 'diff':
            self._order = self._order_diff
        else:
            raise NotImplemented()

    def _order_seq(self, board, moves):
        return moves

    def _order_random(self, board, moves):
        random.shuffle(moves)
        return moves

    def _order_eval(self, board, moves):
        if not hasattr(self, 'evaluate'):
            self.evaluate = Evaluator().evaluate

        if len(moves) <= 1:
            return moves

        return sorted(moves,
                      key=lambda m: -self.evaluate(board.move(m)),
                      reverse=True)

    def _order_diff(self, board, moves):
        if len(moves) <= 1:
            return moves

        return sorted(moves, key=partial(evaldiff, board),
                      reverse=True)

    def order(self, board, moves, hint=None):
        if hint is not None:
            yield hint

        for x in self._order(board, moves):
            if x == hint:
                continue
            yield x
