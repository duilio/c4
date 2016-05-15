from collections import namedtuple, OrderedDict

from c4.evaluate import INF


Entry = namedtuple('Entry', 'move depth score state')


class Cache(object):
    EXACT = object()
    UPPERBOUND = object()
    LOWERBOUND = object()

    def __init__(self, maxitems=50000):
        self._maxitems = maxitems
        self._cache = OrderedDict()

    def put(self, board, moves, depth, ply, score, alpha=-INF, beta=INF):
        key, flip = board.hashkey()
        if moves:
            move = moves[0]
        else:
            move = None
        if flip and move is not None:
            move = 6 - move

        if depth == 0 or depth == -1 or alpha < score < beta:
            state = Cache.EXACT
        elif score >= beta:
            state = Cache.LOWERBOUND
            score = beta
        elif score <= alpha:
            state = Cache.UPPERBOUND
            score = alpha
        else:
            assert False

        entry = Entry(move, depth, int(score), state)
        self._cache.pop(key, None)
        self._cache[key] = entry

        if len(self._cache) > self._maxitems:
            self._cache.popitem(last=False)

    def lookup(self, board, depth, ply, alpha=-INF, beta=INF):
        key, flip = board.hashkey()
        if key not in self._cache:
            return False, None, None

        entry = self._cache[key]

        hit = False
        if entry.depth == -1:
            hit = True
        elif entry.depth >= depth:
            if entry.state is Cache.EXACT:
                hit = True
            elif entry.state is Cache.LOWERBOUND and entry.score >= beta:
                hit = True
            elif entry.state is Cache.UPPERBOUND and entry.score <= alpha:
                hit = True

        if flip and entry.move is not None:
            move = 6 - entry.move
        else:
            move = entry.move

        if hit:
            score = entry.score
        else:
            score = None

        return hit, move, score
