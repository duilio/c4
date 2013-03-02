from c4.evaluate import INF
from c4.cache import Cache


class CachedEngineMixin(object):
    def __init__(self, *args, **kwargs):
        super(CachedEngineMixin, self).__init__(*args, **kwargs)
        self._cache = Cache()

    def search(self, board, depth, ply=1, alpha=-INF, beta=INF):
        hit, move, score = self._cache.lookup(board, depth, ply, alpha, beta)
        if hit:
            self.inc('hits')
            if move is not None:
                move = [move]
            else:
                move = []
            return move, score
        else:
            move, score = super(CachedEngineMixin, self).search(board, depth, ply,
                                                                alpha, beta,
                                                                hint=move)
            self._cache.put(board, move, depth, ply, score, alpha, beta)
            return move, score
