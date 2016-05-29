"""Keras input processors

"""
import numpy as np

from c4.registry import Registry


registry = Registry()


class Processor(object):
    def get_shape(self):
        raise NotImplemented()

    def process(self, board):
        raise NotImplemented()


@registry.add('sides')
class SidesSplitProcessor(object):
    """Simple processor that splits the board in two layers

    Each layer is a binary map with representing the player occupied squares.

    """
    def get_shape(self):
        return (2, 7, 6)

    def process(self, board):
        pos = board.rawdata
        return np.asarray(
            np.stack((pos == board.stm,
                      pos == board.other)),
            dtype=np.uint8)


@registry.add('sidesandmoves')
class SidesAndMovesProcessor(object):
    """Add a layer of allowed moves to the SidesSplitProcessor

    """
    def get_shape(self):
        return (3, 7, 6)

    def process(self, board):
        pos = board.rawdata
        filled_square = pos != 0
        empty_squares = np.logical_not(filled_square)
        available_moves = np.zeros_like(filled_square, dtype=np.bool)

        move_indices = (np.arange(7), np.argmin(filled_square, 1))
        available_moves[move_indices] = 1
        available_moves = np.logical_and(
            available_moves,
            empty_squares)

        return np.asarray(
            np.stack((pos == board.stm,
                      pos == board.other,
                      available_moves)),
            dtype=np.uint8)


@registry.add('sidesandmoves2')
class SidesAndMovesProcessor2(SidesAndMovesProcessor):
    """Like SidesAndMovesProcessor but add also two layers with zeros and ones

    """
    def __init__(self):
        super(SidesAndMovesProcessor2, self).__init__()
        self.zeros = np.zeros((1, 7, 6), dtype=np.uint8)
        self.ones = np.ones((1, 7, 6), dtype=np.uint8)

    def get_shape(self):
        return (5, 7, 6)

    def process(self, board):
        sidesandmoves = super(SidesAndMovesProcessor2, self).process(board)
        return np.concatenate((
            self.zeros,
            sidesandmoves,
            self.ones,
        ))
