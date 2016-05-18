from itertools import permutations

from c4.game import GameHandler


class Stat(object):
    __slots__ = ['win', 'loose', 'draws', 'win_X', 'win_O', 'score']

    def __init__(self):
        self.win = 0
        self.loose = 0
        self.draws = 0
        self.win_X = 0
        self.win_O = 0
        self.score = 0


def arena(engines, rounds):
    DRAW_SCORE = 1
    WIN_SCORE = 3

    stats = {}
    for name, e in engines:
        stats[name] = Stat()

    for round in range(rounds):
        for (n1, e1), (n2, e2) in permutations(engines, 2):
            print("%s vs %s" % (n1, n2))
            game = GameHandler(e1, e2)
            b, winner, looser = game.play()

            if winner is None:
                stats[n1].draws += 1
                stats[n1].score += DRAW_SCORE
                stats[n2].draws += 1
                stats[n2].score += DRAW_SCORE
                continue

            if winner is e1:
                winner_name = n1
                looser_name = n2
            else:
                winner_name = n2
                looser_name = n1

            stats[winner_name].win += 1
            stats[winner_name].score += WIN_SCORE
            if e1 is winner:
                stats[winner_name].win_X += 1
            elif e2 is winner:
                stats[winner_name].win_O += 1

            stats[looser_name].loose += 1

    rank = sorted(stats.items(), key=lambda x: x[1].score, reverse=True)
    formats = '%-3s  | %-16s | %5s | %4s | %4s | %4s'
    print(formats % ('N.', 'Name', 'Score', 'Win', 'WinX', 'WinO'))
    for i, (name, stat) in enumerate(rank, 1):
        print(formats % (i, name, stat.score, stat.win, stat.win_X,
                         stat.win_O))
