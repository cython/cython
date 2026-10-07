#!/usr/bin/env python3

"""Utility code for benchmark scripts."""

import cython

from functools import partial
import sys
import time

# PyPy's JIT can induce high variance so we basically ignore this measure.
IS_PYPY = sys.implementation.name == 'pypy'


def repeat_to_accuracy(func, *args,
                       variance_threshold: float = 1. if IS_PYPY else 5e-5,
                       outlier_threshold: float = .12,
                       scale=1,
                       repeat=True,
                       max_iterations: cython.long = 1_000,
                       min_iterations: cython.long = 5,
                       scale_to=None,
                       ):
    """Repeatedly call and time the function
    until the variance of the timings is below 'variance_threshold'.

    Slow runs that are more than a factor of 'outlier_threshold'
    over the current mean are excluded.

    Returns the calculated mean and the list of timings.
    """
    if not callable(func):
        raise ValueError("need a callable")

    times = []
    call_benchmark = partial(func, *args, scale, time.perf_counter)

    if scale_to is None or scale_to == scale:
        scale_factor = 1.0
    else:
        scale_factor = scale_to / scale

    # First counted run.
    execution_time: float = call_benchmark()
    times.append(execution_time)

    mean: float = execution_time
    variance: float = 0.
    squares: float = 0.

    get_wall_time = time.time

    if repeat:
        # Run for at least 1 wall clock second
        min_runtime = get_wall_time() + 1
    else:
        # Special non-repeat mode for initial auto-scaling.
        max_iterations = min_iterations = 3
        variance_threshold = .1
        outlier_threshold = 10.  # try to exclude nothing
        min_runtime = 0.

    # Put an upper bound on the wall clock runtime as well.
    max_runtime = get_wall_time() + 1 * 30

    count: cython.long
    discarded: cython.long = 0
    for count in range(2, max_iterations + 1):
        # Time the function.
        execution_time = call_benchmark()
        times.append(execution_time)

        # Incrementally calculate mean and sum of squares.
        delta = execution_time - mean

        # Discard extremely slow outliers.
        if mean and delta / mean > outlier_threshold:
            discarded += 1
            continue
        count -= discarded

        mean += delta / count
        delta2 = execution_time - mean
        squares += delta * delta2

        # Calculate variance.
        variance = squares / (count - 1)
        if count < min_iterations:
            continue
        if variance < variance_threshold:
            if get_wall_time() < min_runtime:
                continue
            break
        if get_wall_time() > max_runtime:
            break

    times = [t * scale_factor for t in times]

    return times, mean, variance


def scale_subbenchmarks(timings_by_name, scale):
    """Calculate scaling factors for sub-benchmarks.

    For the intended 'scale' count and a dict of {name:time}
    with a run time measurement for each benchmark,
    return a benchmark specific mapping {name:scale}.
    """
    reference = max(timings_by_name.values())
    return {
        name: int((reference / t) * scale)
        for name, t in timings_by_name.items()
    }


# Original implementation:

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
        import math
        import operator
        from functools import reduce

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
