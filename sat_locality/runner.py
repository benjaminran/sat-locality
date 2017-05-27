"""SAT locality experiment runner"""
import os
import sys
import logging
import argparse
from signal import signal, SIGPIPE, SIG_DFL
import numpy as np
import delegator
import matplotlib.pyplot as plt

from .generators import circle

signal(SIGPIPE, SIG_DFL)


def main():
    # cli options
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('generator', help='one of: circle')
    parser.add_argument('-a', '--min-w', type=float, default=0,
                        help='minimum w')
    parser.add_argument('-b', '--max-w', type=float, default=0.5,
                        help='maximum w')
    parser.add_argument('-s', '--steps', type=float, default=10,
                        help='number of steps between min and max k')
    parser.add_argument('-t', '--trials', type=int, default=3,
                        help='trials per step')
    parser.add_argument('-d', '--experiment-dir', default='experiment',
                        help='directory to write experiment files/results in')
    args, rest = parser.parse_known_args()
    generators = {
       'circle': circle
    }
    # prepare
    os.makedirs(args.experiment_dir)
    logging.basicConfig(
       filename=os.path.join(args.experiment_dir, 'experiment.log'),
       level=logging.DEBUG)
    # run experiment
    logging.info('generating instances and solving')
    instance_number = 1
    for w in np.linspace(args.min_w, args.max_w, num=args.steps + 1):
        if w == 0.0:
            continue
        argw = ['-w', str(w)]
        for trial in range(args.trials):
            logging.debug('instance {} of {}'
                          .format(instance_number, args.steps * args.trials))
            instance_number += 1
            instance = 'trial-{}-{}.cnf'.format(w, trial)
            instance_path = os.path.join(args.experiment_dir, instance)
            result_path = os.path.join(
               args.experiment_dir, 'result-{}-{}.txt'.format(w, trial))
            generators[args.generator].generate(rest + argw, instance_path)
            delegator.run(
               'cat {} | docker run --rm -i msoos/cryptominisat:v2 > {}'
               .format(instance_path, result_path))
    # prepare outputs
    logging.info('analyzing outputs')
    W = []
    times = []
    for dirpath, dirnames, filenames in os.walk(args.experiment_dir):
        trial_times = []
        for result_file in [f for f in filenames if 'result' in f]:
            w = float(result_file.split('-')[1])
            trial = int(result_file.split('-')[2][:-4])
            if trial == 0:
                W.append(w)
            with open(os.path.join(dirpath, result_file)) as f:
                for line in f:
                    if 'c Total time' in line:
                        time = float(line.split(':')[1].strip())
                        trial_times.append(time)
                        break
            if trial == args.trials - 1:
                times.append(sum(trial_times)/len(trial_times))
    # plot results
    plot_file = os.path.join(args.experiment_dir, 'result.png')
    plt.plot(W, times)
    plt.savefig(plot_file)
    logging.info('wrote plot_file ' + plot_file)


if __name__ == '__main__':
    main()
