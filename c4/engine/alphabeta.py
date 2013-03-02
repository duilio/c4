import random

from c4.evaluate import INF, Evaluator
from c4.engine.negamax import NegamaxEngine


class MoveOrder(object):
    def __init__(self, name):
        if name == 'seq':
            self.order = self._order_seq
        elif name == 'random':
            self.order = self._order_random
        elif name == 'eval':
            self.order = self._order_eval
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

        ordered_moves = [(-self.evaluate(board.move(m)), m) for m in moves]
        ordered_moves.sort(reverse=True)
        for _, m in ordered_moves:
            yield m
        

class AlphaBetaEngine(NegamaxEngine):
    FORMAT_STAT = (
        'score: {score} [time: {time}s, pv: {pv}]\n' +
        'nps: {nps}, nodes: {nodes}, betacuts: {betacuts}\n' +
        'leaves: {leaves}, draws: {draws}, mates: {mates}'
        )

    def __init__(self, maxdepth, ordering='seq'):
        super(AlphaBetaEngine, self).__init__(maxdepth)
        self.moveorder = MoveOrder(ordering).order

    def initcnt(self):
        super(AlphaBetaEngine, self).initcnt()
        self._counters['betacuts'] = 0

    def search(self, board, depth, ply=1, alpha=-INF, beta=INF):
        self.inc('nodes')

        if board.end is not None:
            return self.endscore(board, ply)

        if depth <= 0:
            self.inc('leaves')
            return [], self.evaluate(board)

        bestmove = []
        bestscore = alpha
        for m in self.moveorder(board, board.moves()):
            nextmoves, score = self.search(board.move(m), depth-1, ply+1,
                                           -beta, -bestscore)
            score = -score
            if score > bestscore:
                bestscore = score
                bestmove = [m] + nextmoves
            elif not bestmove:
                bestmove = [m] + nextmoves

            if bestscore >= beta:
                self.inc('betacuts')
                break

        return bestmove, bestscore

    def __str__(self):
        return 'AlphaBeta(%s)' % self._maxdepth
