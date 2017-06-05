"""Writes out CNF formula of random localized SAT instances in DIMACS format.

Distributes n variables uniformly randomly around a circle, then generates m
clauses of k variables each, where each clause has a random "center" point on
the circle from which all variables of the clause must be within a certain
distance w.
"""
import sys
import logging
import argparse
import numpy as np
import os
from signal import signal, SIGPIPE, SIG_DFL
import delegator
import matplotlib.pyplot as plt
import cProfile

signal(SIGPIPE, SIG_DFL)


class Variable():
    """
    number: variable identifier
    bearing: [0, 1) bearing clockwise from north
    """
    def __init__(self, number, bearing):
        self.number = number
        self.bearing = bearing


def buffered_random(s=1000000):
    """return a random [0.0,1.0) float from a buffer generated in
    exponentially-growing batches"""
    buffer_size = s
    while True:
        logging.debug("buffering {} random numbers".format(buffer_size))
        offset = 0
        buffer = np.random.uniform(size=buffer_size)
        while offset < buffer.size:
            yield buffer[offset]
            offset += 1
        buffer_size *= 2


def min_k(arr, k, key=lambda x: x, big=None):
    """find smallest k elements in 1-d array l. Intended for small k (uses
    insertion sort). Chokes on empty arr. Chokes if maximum element is
    among the min_k"""
    minima = []
    indices = []
    if big is None:
        big = max(arr, key=key)
    for i in range(k):
        min = big
        argmin = -1
        for j in range(len(arr)):
            if key(arr[j]) < key(min) and j not in indices:
                min = arr[j]
                argmin = j
        minima.append(min)
        indices.append(argmin)
    return [m for m, i in sorted(zip(minima, indices))]


def write_header(outfile, n, m, k, w):
    """write DIMACS header. Record generator, n, m, k, and w"""
    outfile.write('c generator: circle')
    outfile.write('c k: {}\n'.format(k))
    outfile.write('c w: {}\n'.format(w))
    outfile.write('p cnf {} {}\n'.format(n, m))


def build_vars(n):
    """return list of n Variables with random bearing"""
    logging.debug("generating {} variables with random bearing".format(n))
    indices = range(1, n + 1)
    bearings = np.random.uniform(size=n)
    return [Variable(indices[i], bearings[i]) for i in range(n)]


def write_clauses(outfile, vars, m, k, w):
    """write m DIMACS clauses of variables uniformly randomly chosen from the
    distance w from a per-clause randomly-chosen center bearing"""
    rand = buffered_random()
    logging.debug("writing clauses")
    for c in range(m):
        clause_vars = []
        while len(clause_vars) == 0:
            center = next(rand)
            legal_vars = [v for v in vars if abs(v.bearing - center) < w
                          or 1 - abs(v.bearing - center) < w]
            sort_keys = [next(rand) for i in range(len(legal_vars))]
            clause_vars = [v.number for r, v in min_k(
                list(zip(sort_keys, legal_vars)), 5, key=lambda x: x[0])]
        clause = [(-1 if next(rand) < 0.5 else 1) * i
                  for i in clause_vars]
        outfile.write(' '.join([str(i) for i in clause]) + ' 0\n')


def generate(args, outfile=None):
    # main routine
    with open(outfile, 'w') if outfile is not None else sys.stdout as f:
        write_header(f, args.variables, args.clauses, args.arity, args.width)
        vars = build_vars(args.variables)
        write_clauses(f, vars, args.clauses, args.arity, args.width)


def main():
    # cli options
    parser = argparse.ArgumentParser(description=__doc__)
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
    parser.add_argument('-n', '--variables', type=int, default=100000,
                        help='number of variables')
    parser.add_argument('-m', '--clauses', type=int, default=100000,
                        help='number of clauses')
    parser.add_argument('-k', '--arity', type=int, default=5,
                        help='number of variables per clause')
    parser.add_argument('-w', '--width', type=float, default=0.25,
                        help='legal distance of variable from clause center')
    args = parser.parse_args()
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
        args.width = w
        for trial in range(args.trials):
            logging.debug('instance {} of {}'
                          .format(instance_number, args.steps * args.trials))
            instance_number += 1
            instance = 'trial-{}-{}.cnf'.format(w, trial)
            instance_path = os.path.join(args.experiment_dir, instance)
            result_path = os.path.join(
               args.experiment_dir, 'result-{}-{}.txt'.format(w, trial))
            generate(args, instance_path)
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


if __name__ == "__main__":
    # cProfile.run('main()')
    main()
