import numpy as np


all_segments = []
rev_segments = [[] for x in range(8*7)]

_indices = np.arange(8*7).reshape((8, 7))


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
    for di in range(-8, 8):
        diag = idx.diagonal(di)
        add_rev(diag)

all_segments = np.asarray(all_segments)
