#!/usr/bin/env python3

"""Microbenchmark for Python's sequence unpacking."""

# Python imports
import collections
import time

import cython


DEFAULT_TIMER = time.perf_counter


def _single_run(to_unpack, iterations: cython.long):
    x: cython.long
    y: cython.long

    # Unpack to C integers
    c: cython.int
    f: cython.long
    h: cython.size_t

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


@cython.cfunc
def do_unpacking(iterations: cython.long, to_unpack, timer=DEFAULT_TIMER):
    t0 = timer()
    _single_run(to_unpack, iterations)
    t = timer() - t0
    return t


def bm_tuple_unpacking(iterations: cython.int, timer=DEFAULT_TIMER):
    x = tuple(range(10))
    return do_unpacking(iterations, x, timer)


def bm_list_unpacking(iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    return do_unpacking(iterations, x, timer)


def bm_iter_unpacking(iterations: cython.int, timer=DEFAULT_TIMER):
    x = list(range(10))
    _iter = iter
    class Iterable(object):
        def __iter__(self):
            return _iter(x)
    return do_unpacking(iterations, Iterable(), timer)


def test_all(iterations, timer=DEFAULT_TIMER):
    tuple_timings = bm_tuple_unpacking(iterations, timer)
    list_timings = bm_list_unpacking(iterations, timer)
    return [x + y for (x, y) in zip(tuple_timings, list_timings)]


def run_benchmark(repeat=True, scale=20_000):
    from util import repeat_to_accuracy, scale_subbenchmarks

    collected_timings = collections.defaultdict(list)

    timings = {}
    for name, func in globals().items():
        if name.startswith('bm_'):
            timings[name] = func(100)
    scales = scale_subbenchmarks(timings, scale)

    for name, func in globals().items():
        if name.startswith('bm_'):
            collected_timings[name] = repeat_to_accuracy(
                func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
