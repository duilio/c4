from c4.evaluate import Evaluator
from c4.engine.base import Engine


class GreedyEngine(Engine):
    def __init__(self):
        self._evaluator = Evaluator()
        self.evaluate = self._evaluator.evaluate

    def choose(self, board):
        moves = board.moves()
        m = moves[0]
        moves = moves[1:]

        bestmove = m
        bestscore = -self.evaluate(board.move(m))
        
        for m in moves:
            score = -self.evaluate(board.move(m))
            if score > bestscore:
                bestmove = m
                bestscore = score

        print('Bestscore:', bestscore)
        return bestmove

    def __str__(self):
        return 'Greedy'
