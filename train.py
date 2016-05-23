import os
import sys
import random

from argparse import ArgumentParser

import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten


def run():
    parser = ArgumentParser()
    parser.add_argument('files', metavar='INPUT', nargs='+',
                        help='Input files')
    parser.add_argument('-b', '--batch-size', type=int, default=512,
                        help='Batch size')
    parser.add_argument('-e', '--epoch', type=int, default=32,
                        help='NN Epoch')
    parser.add_argument('-v', '--validation-split', type=float, default=0.2,
                        help='Validation split')
    parser.add_argument('-r', '--repeat', dest='unique',
                        default=True, action='store_false',
                        help='Leave input duplicates')
    parser.add_argument('-s', '--seed', dest='seed', default=None,
                        type=int, help='Random generator seed')
    parser.add_argument('-o', '--output', metavar='DIRECTORY',
                        default=None, help='Save the model in that path')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='Override output if already exists')
    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)
        random.seed(args.seed)

    input_data = []
    seen = set()
    dups = 0
    for i, filename in enumerate(args.files, 1):
        print('Reading file %s... (%d/%d)' % (filename, i, len(args.files)))
        with open(filename, 'r') as fin:
            for line in fin:
                if not line.strip() or line.startswith('#'):
                    continue

                serialized_board, move, score = line.split()[:3]
                processed_board = preprocess_board(serialized_board)
                move = int(move)
                if score == '1':
                    score = 1
                elif score == '-1':
                    score = 0
                elif score == '0':
                    score = 0.5
                else:
                    score = None

                key = (serialized_board, move, score)
                if args.unique and key in seen:
                    dups += 1
                    continue
                seen.add(key)

                input_data.append((processed_board, move, score))

    if args.unique:
        print('Found %d over %d duplicates' % (dups, dups + len(seen)))

    random.shuffle(input_data)

    print('Preparing data...')
    X = np.array([x[0] for x in input_data],
                 dtype=np.uint8)
    y = np.array([x[1] for x in input_data], dtype=np.uint8)
    Y = np_utils.to_categorical(y, 7)

    print('Compiling model...')
    model = Sequential()
    model.add(Flatten(input_shape=(2, 7, 6)))
    model.add(Dense(69, input_dim=2*7*6))
    model.add(Activation('relu'))
    model.add(Dense(42, input_dim=2*7*6))
    model.add(Activation('relu'))
    model.add(Dense(7))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print('Training...')
    model.fit(X, Y, batch_size=args.batch_size, nb_epoch=args.epoch, verbose=1,
              validation_split=args.validation_split)

    if args.output is not None:
        print('Saving...')
        if os.path.exists(args.output) and not args.force:
            print('Output directory already exists. Use --force to override.')
            sys.exit(1)

        if not os.path.isdir(args.output):
            os.makedirs(args.output)

        arch_filename = os.path.join(args.output, 'arch.yml')
        weights_filename = os.path.join(args.output, 'weights.h5')

        with open(arch_filename, 'w') as fout:
            fout.write(model.to_yaml())
        model.save_weights(weights_filename, overwrite=True)


def preprocess_board(serialized_board):
    stm = serialized_board[-1]
    if stm == '1':
        other = '2'
    else:
        other = '1'

    return np.array(
        [x == stm for x in serialized_board[:-1]] +
        [x == other for x in serialized_board[:-1]],
        dtype=float).reshape(2, 7, 6)


if __name__ == '__main__':
    sys.exit(run())
