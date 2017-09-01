import os
import sys
import random

from argparse import ArgumentParser

import yaml
import numpy as np

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D


from c4.board import Board
from c4.processors import registry



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
    parser.add_argument('-p', '--processor', default='sides',
                        help='Processor to use for model input generation.')
    args = parser.parse_args()

    # initialize seed for reproducibility
    if args.seed is not None:
        np.random.seed(args.seed)
        random.seed(args.seed)

    # create model input processor
    processor_config = {'class': args.processor}
    processor = registry.get(processor_config)

    dups = 0
    rows = 0

    train_datasets = []
    batches = split_batches(args.files)

    for i, files in enumerate(batches, 1):
        print('Loading batch %d/%d' % (i, len(batches)))

        input_data, batch_dups, batch_rows = load_train_data(files,
                                                             processor,
                                                             args.unique)
        dups += batch_dups
        rows += batch_rows

        X = np.array([x[0] for x in input_data], dtype=np.uint8)
        y = np.array([x[1] for x in input_data], dtype=np.uint8)
        Y = np_utils.to_categorical(y, 7)

        train_datasets.append((X, Y))

    if args.unique:
        print('Found %d dups over %d rows' % (dups, rows))

    print('Compiling model...')
    model = Sequential()
    if 0:
        model.add(Flatten(input_shape=processor.get_shape()))
        model.add(Dense(128))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Dense(69))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Dense(42))
        model.add(Activation('relu'))
        model.add(Dense(7))
        model.add(Activation('softmax'))
    else:
        FILTERS = 36
        CONV_KERNEL_SIZE = 4

        model.add(Convolution2D(FILTERS, CONV_KERNEL_SIZE, CONV_KERNEL_SIZE,
                                border_mode='valid',
                                init='uniform',
                                input_shape=processor.get_shape()))
        model.add(Activation('relu'))
        model.add(Dropout(0.15))
        model.add(Flatten())
        model.add(Dense(100))
        model.add(Activation('relu'))
        model.add(Dropout(0.15))
        model.add(Dense(7))
        model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    print('Training...')
    for X, Y in train_datasets:
        model.fit(X, Y, batch_size=args.batch_size,
                  nb_epoch=args.epoch, verbose=1,
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
            arch = yaml.load(model.to_yaml())
            arch['processor'] = processor_config
            yaml.dump(arch, stream=fout)

        model.save_weights(weights_filename, overwrite=True)


def split_batches(files):
    batches = []
    current_batch = []

    for f in files:
        if f == ',':
            batches.append(current_batch)
            current_batch = []
        else:
            current_batch.append(f)

    if current_batch:
        batches.append(current_batch)

    return batches


def load_train_data(files, processor, unique):
    dups = 0
    rows = 0
    seen = set()

    input_data = []
    for i, filename in enumerate(files, 1):
        print('Reading file %s... (%d/%d)' % (filename, i, len(files)))
        with open(filename, 'r') as fin:
            for line in fin:
                if not line.strip() or line.startswith('#'):
                    continue

                rows += 1

                serialized_board, move, score = line.split()[:3]

                board = Board.loads(serialized_board)
                processed_board = processor.process(board)

                move = int(move)
                if score == '1':
                    score = 1
                elif score == '-1':
                    score = 0
                elif score == '0':
                    score = 0.5
                else:
                    score = None

                key = (serialized_board, move)
                if unique and key in seen:
                    dups += 1
                    continue
                seen.add(key)

                input_data.append((processed_board, move, score))

    random.shuffle(input_data)
    return input_data, dups, rows


if __name__ == '__main__':
    sys.exit(run())

