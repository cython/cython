#!/usr/bin/env python

"""Utility code for benchmark scripts."""

__author__ = "collinwinter@google.com (Collin Winter)"

import math
import operator

try:
    reduce
except NameError:
    from functools import reduce

def run_benchmark(options, num_runs, bench_func, *args):
    """Run the given benchmark, print results to stdout.

    Args:
        options: optparse.Values instance.
        num_runs: number of times to run the benchmark
        bench_func: benchmark function. `num_runs, *args` will be passed to this
            function. This should return a list of floats (benchmark execution
            times).
    """
    if options.profile:
        import cProfile
        prof = cProfile.Profile()
        prof.runcall(bench_func, num_runs, *args)
        prof.print_stats(sort=options.profile_sort)
    else:
        data = bench_func(num_runs, *args)
        if options.take_geo_mean:
            product = reduce(operator.mul, data, 1)
            print(math.pow(product, 1.0 / len(data)))
        else:
            for x in data:
                print(x)


def add_standard_options_to(parser):
    """Add a bunch of common command-line flags to an existing OptionParser.

    This function operates on `parser` in-place.

    Args:
        parser: optparse.OptionParser instance.
    """
    parser.add_option("-n", action="store", type="int", default=100,
                      dest="num_runs", help="Number of times to run the test.")
    parser.add_option("--profile", action="store_true",
                      help="Run the benchmark through cProfile.")
    parser.add_option("--profile_sort", action="store", type="str",
                      default="time", help="Column to sort cProfile output by.")
    parser.add_option("--take_geo_mean", action="store_true",
                      help="Return the geo mean, rather than individual data.")
