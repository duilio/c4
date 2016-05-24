import os
import yaml

import numpy as np
from keras.models import model_from_yaml

from c4.engine.base import Engine
from c4.engine.registry import registry


@registry.add('greedykeras')
class GreedyKerasEngine(Engine):
    DEFAULT_PROCESSOR_CONFIG = {'class': 'simple_processor'}

    def __init__(self, model_path):
        arch_filename = os.path.join(model_path, 'arch.yml')
        weights_filename = os.path.join(model_path, 'weights.h5')
        with open(arch_filename) as fin:
            model_arch = yaml.load(fin)
            processor_config = model_arch.pop(
                'processor',
                self.DEFAULT_PROCESSOR_CONFIG)
            model = model_from_yaml(yaml.dump(model_arch))
        model.load_weights(weights_filename)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        self._model = model

    def choose(self, board):
        X = np.array(
            [x == board.stm for x in board._pos.flat] +
            [x == board.other for x in board._pos.flat],
            dtype=np.uint8
        ).reshape((1, 2, 7, 6))

        pred = np.squeeze(self._model.predict(X))
        print('Predictions: %s' % pred)
        legal_moves = list(board.moves())

        for move in pred.argsort()[::-1]:
            if move in legal_moves:
                return move

        assert False

    def __str__(self):
        return 'SimpleNN'
