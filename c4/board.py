import numpy as np

from c4.tables import rev_segments, all_segments


PLAYER1 = 1
PLAYER2 = 2
DRAW = 0
COMPUTE = -1


class WrongMoveError(Exception):
    pass


class Board(object):
    def __init__(self, pos=None, stm=PLAYER1, end=COMPUTE, cols=7, rows=6):
        if pos is None:
            pos = np.zeros((cols, rows), dtype=int)
        self._pos = pos
        self._stm = stm
        if end == COMPUTE:
            self._end = self._check_end(pos)
        else:
            self._end = end

    @property
    def end(self):
        return self._end

    @property
    def stm(self):
        return self._stm

    @property
    def other(self):
        return PLAYER1 if self._stm != PLAYER1 else PLAYER2

    @classmethod
    def _check_end(cls, pos):
        for seg in cls.segments(pos):
            c = np.bincount(seg)
            if c[0]:
                continue
            if c[PLAYER1] == 4:
                return PLAYER1
            elif c[PLAYER2] == 4:
                return PLAYER2

        if pos.all():
            return DRAW
        else:
            return None

    @classmethod
    def _check_end_around(cls, pos, r, c, side):
        if (cls.segments_around(pos, r, c) == side).all(1).any():
            return side

        if pos.all():
            return DRAW
        else:
            return None

    @classmethod
    def segments(cls, pos):
        if isinstance(pos, Board):
            return cls.segments(pos._pos)
        else:
            pos = pos.flatten()
            return pos[all_segments]

    @classmethod
    def segments_around(cls, pos, r, c):
        if isinstance(pos, Board):
            return cls.segments_around(pos._pos, r, c)
        else:
            idx = c * pos.shape[1] + r
            pos = pos.flatten()
            return pos[rev_segments[idx]]

    def __str__(self):
        disc = {
            0: ' ',
            1: 'X',
            2: 'O'
            }

        s = []
        for row in reversed(self._pos.transpose()):
            s.append(' | '.join(disc[x] for x in row))
        s.append(' | '.join('-'*7))
        s.append(' | '.join(map(str, range(1, 8))))
        s = ['| ' + x + ' |' for x in s]
        s = [i + ' ' + x for i, x in zip('ABCDEFG  ', s)]
        s = '\n'.join(s)

        if self._end is DRAW:
            s += '\n<<< Game over: draw' % [self._end]
        elif self._end is not None:
            s += '\n<<< Game over: %s win' % disc[self._end]
        else:
            s += '\n<<< Move to %s' % disc[self._stm]
        return s

    def move(self, m):
        if not (0 <= m < 7):
            raise ValueError(m)

        pos = self._pos.copy()

        r = pos[m].argmin()
        if pos[m][r] != 0:
            raise WrongMoveError('Full Column')
        pos[m][r] = self._stm
        end = self._check_end_around(pos, r, m, self._stm)
        stm = self.other
        return Board(pos, stm, end)

    def freerow(self, m):
        r = self._pos[m].argmin()
        if self._pos[m][r] != 0:
            return None
        return r

    def moves(self):
        return np.flatnonzero(self._pos[:, -1] == 0)

    def hashkey(self):
        """Generates an hashkey

        Returns a tuple (key, flip)
        flip is True if it returned the key of the symmetric Board.

        """
        k1 = 0
        k2 = 0

        for x in self._pos.flat:
            k1 *= 3
            k1 += int(x)
            assert k1 >= 0

        for x in self._pos[::-1].flat:
            k2 *= 3
            k2 += int(x)
            assert k2 >= 0

        if k2 < k1:
            return k2, True
        else:
            return k1, False
