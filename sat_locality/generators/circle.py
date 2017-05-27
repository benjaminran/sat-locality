"""Writes out CNF formula of random localized SAT instances in DIMACS format.

Distributes n variables uniformly randomly around a circle, then generates m
clauses of k variables each, where each clause has a random "center" point on
the circle from which all variables of the clause must be within a certain
distance w.
"""
import sys
import argparse
import random

from ..model import Variable


def write_header(outfile, n, m, k, w):
    """write DIMACS header. Record generator, n, m, k, and w"""
    outfile.write('c generator: circle')
    outfile.write('c k: {}\n'.format(k))
    outfile.write('c w: {}\n'.format(w))
    outfile.write('p cnf {} {}'.format(n, m))


def build_vars(n):
    """return list of n Variables with random bearing"""
    return [Variable(i + 1, random.random()) for i in range(n)]


def write_clauses(outfile, vars, m, k, w):
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
        outfile.write(' '.join([str(i) for i in clause]) + ' 0\n')


def generate(argv, outfile=None):
    # cli options
    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=sys.argv[0]+' circle')
    parser.add_argument('-n', '--variables', type=int, default=100000,
                        help='number of variables')
    parser.add_argument('-m', '--clauses', type=int, default=100000,
                        help='number of clauses')
    parser.add_argument('-k', '--arity', type=int, default=5,
                        help='number of variables per clause')
    parser.add_argument('-w', '--width', type=float, default=0.25,
                        help='legal distance of variable from clause center')
    args = parser.parse_args(argv)

    # main routine
    with open(outfile, 'w') if outfile is not None else sys.stdout as f:
        write_header(f, args.variables, args.clauses, args.arity, args.width)
        vars = build_vars(args.variables)
        write_clauses(f, vars, args.clauses, args.arity, args.width)


if __name__ == "__main__":
    generate(sys.argv)
