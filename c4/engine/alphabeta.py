from c4.evaluate import INF
from c4.engine.negamax import NegamaxEngine
from c4.moveorder import MoveOrder
        

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
