#!/usr/bin/python
# micro benchmarks for generators

COUNT = 10000

import cython

@cython.locals(N=cython.Py_ssize_t)
def count_to(N):
    for i in range(N):
        yield i

@cython.locals(i=cython.Py_ssize_t)
def round_robin(*_iterators):
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
    return round_robin(*[ count_to(COUNT // i) for i in range(1,N+1) ])

def bm_yield_from(N):
    return yield_from(count_to(N),
                      round_robin(*[ yield_from(count_to(COUNT // i))
                                     for i in range(1,N+1) ]),
                      count_to(N))

def bm_yield_from_nested(N):
    return yield_from(count_to(N),
                      yield_from(count_to(N),
                                 round_robin(*[ yield_from(count_to(COUNT // i))
                                                for i in range(1,N+1) ]),
                                 count_to(N)),
                      count_to(N))


def time(fn, *args):
    from time import time
    begin = time()
    result = list(fn(*args))
    end = time()
    return result, end-begin

def benchmark(N):
    times = []
    for _ in range(N):
        result, t = time(bm_yield_from_nested, 10)
        times.append(t)
    return times

main = benchmark

if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Micro benchmarks for generators."))

    import util
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, benchmark)
