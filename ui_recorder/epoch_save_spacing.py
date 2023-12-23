import math
import argparse


def run(args):
    epoch = 1
    num_saves = 0
    epochs = []
    while epoch <= args.max_epoch:
        # print(epoch)
        epochs.append(epoch)
        num_saves += 1
        epoch = int(math.ceil(epoch * args.ratio))
    print(epochs)
    # print('')
    print('max_epoch', args.max_epoch, 'ratio', args.ratio, 'total saves', num_saves)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ratio', type=float, default=2)
    parser.add_argument('--max-epoch', type=int, default=10000)
    args = parser.parse_args()
    run(args)
