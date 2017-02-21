#!/usr/bin/python3
# cython: language_level=3
# micro benchmarks for coroutines

COUNT = 100000

import cython


async def done(n):
    return n


@cython.locals(N=cython.Py_ssize_t)
async def count_to(N):
    count = 0
    for i in range(N):
        count += await done(i)
    return count


async def await_all(*coroutines):
    count = 0
    for coro in coroutines:
        count += await coro
    return count


@cython.locals(N=cython.Py_ssize_t)
def bm_await_nested(N):
    return await_all(
        count_to(N),
        await_all(
            count_to(N),
            await_all(*[count_to(COUNT // i) for i in range(1, N+1)]),
            count_to(N)),
        count_to(N))


def await_one(coro):
    a = coro.__await__()
    try:
        while True:
            await_one(next(a))
    except StopIteration as exc:
        result = exc.args[0] if exc.args else None
    else:
        result = 0
    return result


def time(fn, *args):
    from time import time
    begin = time()
    result = await_one(fn(*args))
    end = time()
    return result, end-begin


def benchmark(N):
    times = []
    for _ in range(N):
        result, t = time(bm_await_nested, 1000)
        times.append(t)
        assert result == 8221043302, result
    return times


main = benchmark

if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Micro benchmarks for generators.")

    import util
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, benchmark)
