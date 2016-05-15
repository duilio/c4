import time
from collections import defaultdict

from c4.board import DRAW
from c4.evaluate import INF
from c4.engine.greedy import GreedyEngine


class NegamaxEngine(GreedyEngine):
    FORMAT_STAT = (
        'score: {score} [time: {time:0.3f}s, pv: {pv}]\n' +
        'nps: {nps}, nodes: {nodes}, leaves: {leaves}, draws: {draws}, mates: {mates}'
        )

    def __init__(self, maxdepth=4):
        super(NegamaxEngine, self).__init__()
        self._maxdepth = int(maxdepth)

    def choose(self, board):
        self.initcnt()
        pv, score = self.search(board, self._maxdepth)

        self.showstats(pv, score)
        
        return pv[0]

    def initcnt(self):
        self._startt = time.time()
        self._counters = cnt = defaultdict(int)
        cnt['nodes'] = 0
        cnt['leaves'] = 0
        cnt['draws'] = 0
        cnt['mates'] = 0

    def inc(self, cnt):
        self._counters[cnt] += 1

    def showstats(self, pv, score):
        t = time.time() - self._startt
        if t:
            nps = self._counters['nodes'] / t
        else:
            nps = 0

        pv = ', '.join(str(x+1) for x in pv)

        ctx = self._counters.copy()
        ctx['pv'] = pv
        ctx['nps'] = nps
        ctx['score'] = score
        ctx['time'] = t
        
        print(self.FORMAT_STAT.format(**ctx))
    
    def search(self, board, depth, ply=1):
        self.inc('nodes')

        if board.end is not None:
            return self.endscore(board, ply)

        if depth <= 0:
            self.inc('leaves')
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

    def endscore(self, board, ply):
        self.inc('leaves')
        if board.end == DRAW:
            self.inc('draws')
            return [], 0
        else:
            self.inc('mates')
            return [], -(INF - ply)

    def __str__(self):
        return 'Negamax(%s)' % self._maxdepth
