#!/usr/bin/env python

"""Simple, brute-force N-Queens solver."""

__author__ = "collinwinter@google.com (Collin Winter)"

# Python imports
import optparse
import re
import string
from time import time

# Local imports
import util

import cython

try:
    from builtins import range as _xrange
except ImportError:
    from __builtin__ import xrange as _xrange

# Pure-Python implementation of itertools.permutations().
@cython.locals(n=int, i=int, j=int)
def permutations(iterable):
    """permutations(range(3), 2) --> (0,1) (0,2) (1,0) (1,2) (2,0) (2,1)"""
    pool = tuple(iterable)
    n = len(pool)
    indices = list(range(n))
    cycles = list(range(1, n+1))[::-1]
    yield [ pool[i] for i in indices ]
    while n:
        for i in reversed(range(n)):
            j = cycles[i] - 1
            if j == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                cycles[i] = j
                indices[i], indices[-j] = indices[-j], indices[i]
                yield [ pool[i] for i in indices ]
                break
        else:
            return

# From http://code.activestate.com/recipes/576647/
@cython.locals(queen_count=int, i=int, vec=list)
def n_queens(queen_count):
    """N-Queens solver.

    Args:
        queen_count: the number of queens to solve for. This is also the
            board size.

    Yields:
        Solutions to the problem. Each yielded value is looks like
        (3, 8, 2, 1, 4, ..., 6) where each number is the column position for the
        queen, and the index into the tuple indicates the row.
    """
    cols = list(range(queen_count))
    for vec in permutations(cols):
        if (queen_count == len({ vec[i]+i for i in cols })
                        == len({ vec[i]-i for i in cols })):
            yield vec


def test_n_queens(iterations):
    # Warm-up runs.
    list(n_queens(8))
    list(n_queens(8))

    times = []
    for _ in _xrange(iterations):
        t0 = time()
        list(n_queens(8))
        t1 = time()
        times.append(t1 - t0)
    return times

main = test_n_queens

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of an N-Queens solvers."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_n_queens)
