import time

from c4.board import DRAW
from c4.engine.greedy import GreedyEngine

INF = 1000


class NegamaxEngine(GreedyEngine):
    def __init__(self, maxdepth=4):
        super(NegamaxEngine, self).__init__()
        self._maxdepth = maxdepth

    def choose(self, board):
        self._nodes = 0
        self._leaves = 0
        self._draws = 0
        self._mates = 0
        startt = time.time()

        pv, score = self.search(board, self._maxdepth)

        t = time.time() - startt
        if t:
            nps = self._nodes / t
        else:
            nps = 0
        
        print 'score: %s [time: %s, pv: %s]' % (score, t,
                                                ', '.join(str(x+1) for x in pv))
        print 'nps: %s, nodes: %s, leaves: %s, draws: %s, mates: %s' % (nps,
                                                                        self._nodes,
                                                                        self._leaves,
                                                                        self._draws,
                                                                        self._mates)
        return pv[0]

    def search(self, board, depth, ply=1):
        self._nodes += 1

        if board.end is not None:
            self._leaves += 1

            if board.end == DRAW:
                self._draws += 1
                return [], 0
            else:
                self._mates += 1
                return [], -(INF - ply)

        if depth <= 0:
            self._leaves += 1
            return [], self.evaluate(board)

        bestmove = []
        bestscore = -INF
        for m in board.moves():
            nextmoves, score = self.search(board.move(m), depth-1, ply+1)
            score = -score
            if not bestmove or score >= bestscore:
                bestscore = score
                bestmove = [m] + nextmoves

        return bestmove, bestscore
