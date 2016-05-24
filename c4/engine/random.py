import random

from c4.evaluate import Evaluator
from c4.engine.base import Engine
from c4.engine.registry import registry


@registry.add('random')
class RandomEngine(Engine):
    def __init__(self):
        self._evaluator = Evaluator()
        self.evaluate = self._evaluator.evaluate

    def choose(self, board):
        moves = board.moves()
        return random.choice(moves)

    def __str__(self):
        return 'Random'
