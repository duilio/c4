from itertools import chain

import numpy as np


PLAYER1 = 1
PLAYER2 = 2
DRAW = 0


class WrongMoveError(Exception):
    pass


class Board(object):
    def __init__(self, pos=None, stm=PLAYER1, cols=8, rows=7):
        if pos is None:
            pos = np.zeros((cols, rows), dtype=int)
        self._pos = pos
        self._stm = stm
        self._end = self._check_end(pos)
        
    @property
    def end(self):
        return self._end

    @property
    def stm(self):
        return self._stm

    @classmethod
    def _check_end(cls, pos):
        for seg in cls.segments(pos):
            if (seg == PLAYER1).all():
                return PLAYER1
            elif (seg == PLAYER2).all():
                return PLAYER2

        if (pos == 0).any():
            return None
        else:
            return DRAW

    @classmethod
    def linear_segments(cls, line):
        for x in range(len(line) - 3):
            yield line[x:x+4]

    @classmethod
    def segments(cls, pos):
        if isinstance(pos, Board):
            for x in cls.segments(pos._pos):
                yield x
        else:
            # vertical segments
            for col in pos:
                for x in cls.linear_segments(col):
                    yield x

            # horizontal segments
            for row in pos.transpose():
                for x in cls.linear_segments(row):
                    yield x

            # diagonal segments
            invpos = pos[:, ::-1]
            for d in range(-(len(pos) - 4), (len(pos) - 4)):
                diag1 = pos.diagonal(d)
                diag2 = invpos.diagonal(d)
                for x in chain(cls.linear_segments(diag1),
                               cls.linear_segments(diag2)):
                    yield x

    def __str__(self):
        disc = {
            0: ' ',
            1: 'X',
            2: 'O'
            }

        s = []
        for row in reversed(self._pos.transpose()):
            s.append(' | '.join(disc[x] for x in row))
        s.append(' | '.join('-'*8))
        s.append(' | '.join(map(str, range(1, 9))))
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
        if not (0 <= m < 8):
            raise ValueError(m)

        pos = self._pos.copy()

        r = pos[m].argmin()
        if pos[m][r] != 0:
            raise WrongMoveError('Full Column')
        pos[m][r] = self._stm
        stm = PLAYER1 if self._stm != PLAYER1 else PLAYER2
        return Board(pos, stm)

    def moves(self):
        return np.flatnonzero(self._pos[:, -1] == 0)
