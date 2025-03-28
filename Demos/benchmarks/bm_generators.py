#!/usr/bin/python
# micro benchmarks for generators

COUNT = 20_000

import cython
import time


def count_to(N: cython.Py_ssize_t):
    i: cython.Py_ssize_t
    for i in range(N):
        yield i

def round_robin(*_iterators):
    i: cython.Py_ssize_t

    iterators = list(_iterators)
    to_drop = []

    while iterators:
        for i, it in enumerate(iterators):
            try:
                value = next(it)
            except StopIteration:
                to_drop.append(i)
            else:
                yield value
        if to_drop:
            for i in reversed(to_drop):
                del iterators[i]
            del to_drop[:]


def yield_from(*iterators):
    for it in iterators:
        yield from it


def bm_plain(N):
    return count_to(COUNT * N)

def bm_round_robin(N):
    i: cython.Py_ssize_t
    return round_robin(*[ count_to(COUNT // i) for i in range(1,N+1) ])

def bm_yield_from(N):
    i: cython.Py_ssize_t
    return yield_from(count_to(N),
                      round_robin(*[ yield_from(count_to(COUNT // i))
                                     for i in range(1,N+1) ]),
                      count_to(N))

def bm_yield_from_nested(N):
    i: cython.Py_ssize_t
    return yield_from(count_to(N),
                      yield_from(count_to(N),
                                 round_robin(*[ yield_from(count_to(COUNT // i))
                                                for i in range(1,N+1) ]),
                                 count_to(N)),
                      count_to(N))


def time_func(fn, N, scale: cython.long = 1, timer=time.perf_counter):
    s: cython.long
    result = None

    begin = timer()
    for s in range(scale):
        result = list(fn(N))
    end = timer()
    return result, end - begin


def benchmark(N, count=10, scale=1, timer=time.perf_counter):
    times = []
    for _ in range(N):
        result, t = time_func(bm_yield_from_nested, count, scale=scale)
        times.append(t)
    return times

main = benchmark


def run_benchmark(repeat=10, scale=1, timer=time.perf_counter):
    return benchmark(repeat, count=200, scale=scale, timer=timer)


if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Micro benchmarks for generators."))

    import util
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, benchmark)
