import random

from c4.board import Board
from c4.evaluate import Evaluator, INF


class MoveOrder(object):
    def __init__(self, name):
        if name == 'seq':
            self.order = self._order_seq
        elif name == 'random':
            self.order = self._order_random
        elif name == 'eval':
            self.order = self._order_eval
        elif name == 'diff':
            self.order = self._order_diff
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

        ordered_moves = [(-self.evaluate(board.move(m)), m) for m in moves]
        ordered_moves.sort(reverse=True)
        for _, m in ordered_moves:
            yield m

    def _order_diff(self, board, moves):
        def evaldiff(m):
            r = board.freerow(m)
            stm = board.stm
            score = 0
            for s in Board.segments_around(board, r, m):
                z = (s == 0).sum() - 1
                c = (s == stm).sum() + 1
                assert z >= 0
                if c + z == 4:
                    # add player advantages on this area
                    if c == 4:
                        return INF
                    score += (c-1) ** 2
                else:
                    # remove enemy advantages on this area
                    c = 4 - (c+z)
                    z += 1
                    assert 1 <= c < 4
                    if c + z == 4:
                        score += (c-1) ** 2

            return score
                    
        if len(moves) <= 1:
            return moves

        ordered_moves = [(evaldiff(m), m) for m in moves]
        ordered_moves.sort(reverse=True)
        for _, m in ordered_moves:
            yield m
