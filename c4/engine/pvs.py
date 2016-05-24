from c4.evaluate import INF
from c4.engine.alphabeta import AlphaBetaEngine
from c4.engine.cached import CachedEngineMixin
from c4.engine.deepening import IterativeDeepeningEngineMixin
from c4.engine.book import BookEngineMixin
from c4.engine.registry import registry


@registry.add('pvs')
class PVSEngine(AlphaBetaEngine):
    def search(self, board, depth, ply=1, alpha=-INF, beta=INF, hint=None):
        self.inc('nodes')

        if board.end is not None:
            return self.endscore(board, ply)

        if depth <= 0:
            self.inc('leaves')
            return [], self.evaluate(board)

        bestmove = []
        bestscore = alpha
        for i, m in enumerate(self.moveorder(board, board.moves(), hint)):
            if i == 0 or depth == 1 or (beta-alpha) == 1:
                nextmoves, score = self.search(board.move(m), depth-1, ply+1,
                                               -beta, -bestscore)
            else:
                # pvs uses a zero window for all the other searches
                _, score = self.search(board.move(m), depth-1, ply+1,
                                       -bestscore-1, -bestscore)
                score = -score
                if score > bestscore:
                    nextmoves, score = self.search(
                        board.move(m), depth-1, ply+1,
                        -beta, -bestscore)
                else:
                    continue

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
        return 'PVS(%s)' % self._maxdepth


@registry.add('pvscached')
class PVSCachedEngine(CachedEngineMixin, PVSEngine):
    FORMAT_STAT = (
        'score: {score} [time: {time:0.3f}s, pv: {pv}]\n' +
        'nps: {nps}, nodes: {nodes}, betacuts: {betacuts}\n' +
        'hits: {hits}, leaves: {leaves}, draws: {draws}, mates: {mates}'
        )

    def initcnt(self):
        super(PVSCachedEngine, self).initcnt()
        self._counters['hits'] = 0

    def __str__(self):
        return 'PVSCache(%s)' % self._maxdepth


@registry.add('pvsdeep')
class PVSDeepEngine(CachedEngineMixin, IterativeDeepeningEngineMixin,
                    PVSEngine):
    FORMAT_STAT = (
        '[depth: {depth}] score: {score} [time: {time:0.3f}s, pv: {pv}]\n' +
        'nps: {nps}, nodes: {nodes}, betacuts: {betacuts}\n' +
        'hits: {hits}, leaves: {leaves}, draws: {draws}, mates: {mates}'
        )

    def initcnt(self):
        super(PVSDeepEngine, self).initcnt()
        self._counters['hits'] = 0

    def __str__(self):
        return 'PVSDeep(%s)' % self._maxdepth


@registry.add('pvsbook')
class PVSBookEngine(BookEngineMixin, PVSDeepEngine):
    def __str__(self):
        return 'PVSBook(%s)' % self._maxdepth
