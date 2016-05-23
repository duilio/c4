"""Read some game logs and write all positions with all forced moves

NOTE: Consider only forced moves due to a threat or the ones that make
      the player win.

"""
from __future__ import print_function
import os
import sys
import random

from argparse import ArgumentParser
from itertools import chain

from c4.board import Board
from c4.evaldiff import evaldiff, INF


def iter_files(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.game'):
                yield os.path.join(root, f)


def run():
    parser = ArgumentParser()
    parser.add_argument('paths', metavar='DIRECTORY', nargs='+')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()

    fout = sys.stdout
    if args.output:
        fout = open(args.output, 'w')

    gamefiles = list(chain.from_iterable(
        iter_files(path) for path in args.paths))

    try:
        for i, filename in enumerate(gamefiles, 1):
            print(
                '=== Processing file %s/%s (%.2f%%)' % (
                    i,
                    len(gamefiles),
                    i/len(gamefiles) * 100),
                file=sys.stderr
            )
            process(filename, fout)
            fout.flush()
    finally:
        fout.close()


def process(filename, fout):
    with open(filename, 'r') as fin:
        moves = [int(x.strip()) for x in fin.readlines() if x.strip()]
        board = Board()
        for m in moves[:-1]:
            board = board.move(m)
            for forced_move, win in iter_forced_move(board):
                score = '1' if win else '-'
                print('\t'.join([board.dumps(), str(forced_move),
                                 score]),
                      file=fout)
        assert board.end is None


def iter_forced_move(board):
    scores = sorted(((evaldiff(board, m), m) for m in board.moves()),
                    reverse=True)
    if scores[0][0] == INF:
        for score, m in scores:
            if score != INF:
                return
            else:
                yield m, True

    if scores[0][0] == INF - 1:
        if sum(s == INF - 1 for s, _ in scores) > 1:
            return
        else:
            yield scores[0][1], False


if __name__ == '__main__':
    sys.exit(run())
