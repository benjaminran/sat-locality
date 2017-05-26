#!/usr/bin/env python3
"""Writes out CNF formula of random localized SAT instances in DIMACS format.

Distributes n variables uniformly randomly around a circle, then generates m
clauses of k variables each, where each clause has a random "center" point on
the circle from which all variables of the clause must be within a certain
distance w.
"""
import sys
import argparse
import random
from signal import signal, SIGPIPE, SIG_DFL

__version__ = '0.0.1'
signal(SIGPIPE, SIG_DFL)


class Variable():
    """
    number: variable identifier
    bearing: [0, 1) bearing clockwise from north
    """
    def __init__(self, number, bearing):
        self.number = number
        self.bearing = bearing


def write_header(n, m, k, w):
    """write DIMACS header. Record n, m, k, and w in comments"""
    print('c generator: circle')
    print('c version: ' + __version__)
    print('c k: ' + str(k))
    print('c w: ' + str(w))
    print('p cnf {} {}'.format(n, m))


def build_vars(n):
    """return list of n Variables with random bearing"""
    return [Variable(i + 1, random.random()) for i in range(n)]


def write_clauses(vars, m, k, w):
    """write m DIMACS clauses of variables uniformly randomly chosen from the
    distance w from a per-clause randomly-chosen center bearing"""
    for c in range(m):
        clause_vars = []
        while len(clause_vars) == 0:
            center = random.random()
            legal_vars = [(random.random(), v) for v in vars
                          if abs(v.bearing - center) < w]
            clause_vars = [v[1].number for v in sorted(
                legal_vars, key=lambda x: x[0])][:5]
        clause = [(-1 if random.random() < 0.5 else 1) * i
                  for i in clause_vars]
        sys.stdout.write(' '.join([str(i) for i in clause]) + ' 0\n')


if __name__ == "__main__":
    # cli options
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(
                            version=__version__))
    parser.add_argument('-n', '--variables', type=int, default=100000,
                        help='number of variables')
    parser.add_argument('-m', '--clauses', type=int, default=100000,
                        help='number of clauses')
    parser.add_argument('-k', '--arity', type=int, default=5,
                        help='number of variables per clause')
    parser.add_argument('-w', '--width', type=float, default=0.25,
                        help='legal distance of variable from clause center')
    args = parser.parse_args()

    # main routine
    write_header(args.variables, args.clauses, args.arity, args.width)
    vars = build_vars(args.variables)
    write_clauses(vars, args.clauses, args.arity, args.width)
