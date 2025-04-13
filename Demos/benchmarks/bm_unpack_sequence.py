#!/usr/bin/env python

"""Microbenchmark for Python's sequence unpacking."""

# Python imports
import optparse
import time

import cython


DEFAULT_TIMER = time.perf_counter


@cython.cfunc
def do_unpacking(repeat: cython.long, iterations: cython.long, to_unpack, timer=DEFAULT_TIMER):
    x: cython.long
    y: cython.long

    # Unpack to C integers
    c: cython.int
    f: cython.long
    h: cython.size_t

    times = []
    for x in range(repeat):
        t0 = timer()
        for y in range(iterations):
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack

            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
            a, b, c, d, e, f, g, h, i, j = to_unpack
        t = timer() - t0
        times.append(t)
    return times


def test_tuple_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = tuple(range(10))
    return do_unpacking(repeat, iterations, x, timer)


def test_list_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    return do_unpacking(repeat, iterations, x, timer)


def test_iter_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    _iter = iter
    class Iterable(object):
        def __iter__(self):
            return _iter(x)
    return do_unpacking(repeat, iterations, Iterable(), timer)


def test_all(repeat, iterations, timer=time.perf_counter):
    tuple_timings = test_tuple_unpacking(repeat, iterations, timer)
    list_timings = test_list_unpacking(repeat, iterations, timer)
    return [x + y for (x, y) in zip(tuple_timings, list_timings)]


def run_benchmark(repeat=10, scale=20_000, timer=DEFAULT_TIMER):
    return test_all(repeat, scale, timer)


if __name__ == "__main__":
    import util
    parser = optparse.OptionParser(
        usage="%prog [options] [test]",
        description=("Test the performance of sequence unpacking."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    tests = {"tuple": test_tuple_unpacking, "list": test_list_unpacking}

    if len(args) > 1:
        parser.error("Can only specify one test")
    elif len(args) == 1:
        func = tests.get(args[0])
        if func is None:
            parser.error("Invalid test name")
        util.run_benchmark(options, options.num_runs, func)
    else:
        util.run_benchmark(options, options.num_runs, test_all)
