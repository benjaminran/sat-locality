"""SAT locality experiment runner"""
import sys
import argparse
from signal import signal, SIGPIPE, SIG_DFL

from ..generators import circle

signal(SIGPIPE, SIG_DFL)


def main():
    # cli options
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('generator', help='one of: circle')
    args, unknown = parser.parse_known_args()
    generators = {
       'cirle': circle.main
    }
    generators[args.generator]()

if __name__ == '__main__':
    main()
