import numpy as np
import itertools

#
# Segment tables
#
# Segments are quartets of indices that represent four squares aligned and
# consecutive in the board.
# If a segment contains piece of the same player, that player won the game.
#
# all_segments is a 2d array, each row is a segment
# rev_segments is an index square -> group of segments that pass by the square
#

all_segments = []
rev_segments = [[] for x in range(7*6)]

_indices = np.arange(7*6).reshape((7, 6))


def add_rev(line):
    for x in range(len(line)-3):
        seg = line[x:x+4]
        all_segments.append(seg)
        for n in seg:
            rev_segments[n].append(seg)

for col in _indices:
    add_rev(col)

for row in _indices.transpose():
    add_rev(row)

for idx in (_indices, _indices[:, ::-1]):
    for di in range(-7, 7):
        diag = idx.diagonal(di)
        add_rev(diag)


all_segments = np.asarray(all_segments)
rev_segments = np.asarray([np.asarray(x) for x in rev_segments])


#
# evaldiff lookup tables
#

# keep the scores of segment combos
evaldiff_lookup = {
    1: np.zeros(3**4, dtype=int),
    2: np.zeros(3**4, dtype=int),
}
# used to check if the opponent would win if we don't fill the empty square
evaldiff_threat_lookup = {
    1: np.zeros(3**4, dtype=int),
    2: np.zeros(3**4, dtype=int),
}

for comb in itertools.product(range(3), range(3), range(3), range(3)):
    c = [0, 0, 0]
    score1 = 0
    score2 = 0

    for x in comb:
        c[x] += 1

    if c[0] == 4:
        score1 = 1
        score2 = 1
    elif c[0] + c[1] == 4:
        score1 = (c[1] + 1) ** 2
        score2 = c[1] ** 2
    elif c[0] + c[2] == 4:
        score2 = (c[2] + 1) ** 2
        score1 = c[2] ** 2

    key = np.dot(np.array(comb, dtype=int),
                 np.array([3**0, 3**1, 3**2, 3**3], dtype=int))
    evaldiff_lookup[1][key] = score1
    evaldiff_lookup[2][key] = score2
    if score2 == 4 ** 2:
        evaldiff_threat_lookup[1][key] = 1
    elif score1 == 4 ** 2:
        evaldiff_threat_lookup[2][key] = 1
