import math
from collections import defaultdict

from c4.engine.base import Engine
from c4.engine.greedy import WeightedGreedyEngine
#from c4.engine.random import RandomEngine
from c4.evaluate import DRAW


class MonteCarloTreeSearch(Engine):
    def __init__(self, simulations=1000, C=1/math.sqrt(2)):
        super(MonteCarloTreeSearch, self).__init__()
        self.simulations = int(simulations)
        self.C = float(C)
        self.simulation_engine = WeightedGreedyEngine(False)
        self._stats = defaultdict(lambda: [0, 0])

    def choose(self, board):
        stats, depth = self.search(board, self.simulations, self.C)
        return self.select_best_move(stats, depth, board)

    def search(self, board, simulations, C):
        stats = self._stats
        root = board
        max_depth = 0

        for i in range(simulations):
            node = root
            states = [node.hashkey()]
            transactions = []

            # select leaf node
            depth = 0
            while node.end is None:
                move, select = self.select_next_move(stats, node, C)
                transactions.append(move)
                node = node.move(move)
                states.append(node.hashkey())

                if not select:
                    break

                depth += 1
            max_depth = max(depth, max_depth)

            # run simulation if not at the end of the game tree
            if node.end is None:
                result = self.simulate(node)
            else:
                if node.end == 0:
                    result = 0.5
                else:
                    result = 0

            # propagate results
            for state, move in list(zip(states[:-1], transactions))[::-1]:
                result = 1 - result
                stats[state, move][0] += 1
                stats[state, move][1] += result

        return stats, max_depth

    def simulate(self, board):
        engine = self.simulation_engine
        node = board
        while node.end is None:
            m = engine.choose(node)
            node = node.move(m)

        if node.end == DRAW:
            return 0.5
        elif node.end == board.stm:
            return 1
        else:
            return 0

    def select_next_move(self, stats, board, C):
        """Select the next state and consider if it should be expanded"""

        k = board.hashkey()
        bestscore = None
        bestmove = None
        total_n = sum(stats[k, m][0] for m in board.moves())

        for m in board.moves():
            n, w = stats[k, m]
            if n == 0:
                return m, False
            else:
                score = (w / n) + C * math.sqrt(2 * math.log(total_n) / n)
                if bestscore is None or score > bestscore:
                    bestscore = score
                    bestmove = m

        assert bestmove is not None
        return bestmove, True

    def select_best_move(self, stats, depth, board):
        """Select the best move at the end of the Monte Carlo tree search"""

        bestscore = 0
        bestmove = None
        k = board.hashkey()
        total_n = 0
        for m in board.moves():
            n, w = stats[k, m]
            total_n += n
            print('Move %d score: %d/%d (%0.1f%%)' % (m+1, w, n, w/n*100))
            if n > bestscore:
                bestmove = m
                bestscore = n
        assert bestmove is not None

        print('Maximum depth: %d, Total simulations: %d' % (depth, total_n))

        return bestmove

    def __str__(self):
        return 'MCTS(%s, %0.2f)' % (self.simulations, self.C)
