class IterativeDeepeningEngineMixin(object):
    def choose(self, board):
        for depth in range(1, self._maxdepth+1):
            self.initcnt()
            self._counters['depth'] = depth
            pv, score = self.search(board, depth)
            self.showstats(pv, score)
        return pv[0]
