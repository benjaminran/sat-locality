"""Writes out CNF formula of random localized SAT instances in DIMACS format.

Distributes n variables uniformly randomly around a circle then generates m
clauses of a variables each where each clause has a random "center" point on
the circle from which all variables in the clause must be within a certain
distance w.
"""
import sys
import logging
import argparse
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
import bisect

signal(SIGPIPE, SIG_DFL)


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
    outfile.write('c generator: circle\n')
    outfile.write('c k: {}\n'.format(k))
    outfile.write('c w: {}\n'.format(w))
    outfile.write('p cnf {} {}\n'.format(n, m))


def build_vars(n):
    """return list of n random bearings"""
    logging.debug("generating {} random bearings".format(n))
    return sorted(np.random.uniform(size=n))


def write_clauses(outfile, vars, m, k, w):
    """write m DIMACS clauses of variables uniformly randomly chosen from the
    distance w from a per-clause randomly-chosen center bearing"""
    rand = buffered_random()
    logging.debug("writing clauses")
    for c in range(m):
        center = next(rand)

        lo = bisect.bisect_left(vars, (center - w) % 1)
        hi = bisect.bisect_right(vars, (center + w) % 1)
        if w >= 0.5: lo, hi = 0, len(vars)
        
        legal_indices = None
        if hi < lo:  # crosses edge
            legal_indices = [i for i in range(0, hi)] + [i for i in range(lo, len(vars))]
        else:
            legal_indices = [i for i in range(lo, hi)]
        clause_indices = np.random.choice(legal_indices, size=(k,), replace=False)
        clause = [(-1 if next(rand) < 0.5 else 1) * (i + 1) for i in clause_indices]
        outfile.write(' '.join([str(i) for i in clause]) + ' 0\n')


def generate(args):
    # main routine
    f = open(args.output, 'w') if args.output is not None else sys.stdout
    write_header(f, args.variables, args.clauses, args.arity, args.width)
    vars = build_vars(args.variables)
    write_clauses(f, vars, args.clauses, args.arity, args.width)
    if args.output is not None: f.close()


def main():
    # cli options
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--arity', type=int, default=5,
                        help='number of variables per clause')
    parser.add_argument('-m', '--clauses', type=int, default=100000,
                        help='number of clauses')
    parser.add_argument('-n', '--variables', type=int, default=100000,
                        help='number of variables')
    parser.add_argument('-o', '--output', help='output file name')
    parser.add_argument('-q', '--quiet', action="store_false", dest="verbose",
                        default=True, help='quiet logging')
    parser.add_argument('-p', '--profile', action="store_true", dest="profile",
                        default=False, help='quiet logging')
    parser.add_argument('-w', '--width', type=float, default=0.25,
                        help='legal distance of variable from clause center')
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING)
    # generate
    generate(args)


if __name__ == "__main__":
    main()
