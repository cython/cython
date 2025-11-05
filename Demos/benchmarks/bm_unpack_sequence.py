#!/usr/bin/env python3

"""Microbenchmark for Python's sequence unpacking."""

# Python imports
import collections
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


def bm_tuple_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = tuple(range(10))
    return do_unpacking(repeat, iterations, x, timer)


def bm_list_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    return do_unpacking(repeat, iterations, x, timer)


def bm_iter_unpacking(repeat: cython.int, iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    _iter = iter
    class Iterable(object):
        def __iter__(self):
            return _iter(x)
    return do_unpacking(repeat, iterations, Iterable(), timer)


def test_all(repeat, iterations, timer=DEFAULT_TIMER):
    tuple_timings = bm_tuple_unpacking(repeat, iterations, timer)
    list_timings = bm_list_unpacking(repeat, iterations, timer)
    return [x + y for (x, y) in zip(tuple_timings, list_timings)]


def run_benchmark(repeat: cython.int = 10, number=20_000, timer=DEFAULT_TIMER):
    collected_timings = collections.defaultdict(list)

    for name, func in globals().items():
        if name.startswith('bm_'):
            collected_timings[name] = func(repeat, number, timer)

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")


if __name__ == "__main__":
    import util
    parser = optparse.OptionParser(
        usage="%prog [options] [test]",
        description=("Test the performance of sequence unpacking."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    tests = {"tuple": bm_tuple_unpacking, "list": bm_list_unpacking}

    if len(args) > 1:
        parser.error("Can only specify one test")
    elif len(args) == 1:
        func = tests.get(args[0])
        if func is None:
            parser.error("Invalid test name")
        util.run_benchmark(options, options.num_runs, func)
    else:
        util.run_benchmark(options, options.num_runs, test_all)
