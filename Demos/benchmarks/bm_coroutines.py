#!/usr/bin/python3
# cython: language_level=3
# micro benchmarks for coroutines

COUNT = 100_000

import cython

import time


async def done(n):
    return n


async def count_to(N: cython.Py_ssize_t):
    count = 0
    for i in range(N):
        count += await done(i)
    return count


async def await_all(*coroutines):
    count = 0
    for coro in coroutines:
        count += await coro
    return count


def bm_await_nested(N: cython.Py_ssize_t):
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
    return result


def time_bm(fn, *args, scale: cython.long = 1, timer=time.perf_counter):
    s: cython.long
    result = None
    begin = timer()
    for s in range(scale):
        result = await_one(fn(*args))
    end = timer()
    return result, end - begin


_RESULT_BY_COUNT = {
    1_000: 8221043302,
    100: 8174538781,
    10: 7748658728,
}

def benchmark(N, count=100, scale=1, timer=time.perf_counter):
    times = []
    expected_result = _RESULT_BY_COUNT[count]
    for _ in range(N):
        result, t = time_bm(bm_await_nested, count, scale=scale, timer=timer)
        times.append(t)
        assert result == expected_result, (expected_result, result)
    return times


def run_benchmark(repeat=True, scale=1):
    from util import repeat_to_accuracy

    count = 100
    expected_result = _RESULT_BY_COUNT[count]

    def single_run(scale, timer):
        result, t = time_bm(bm_await_nested, count, scale=scale, timer=timer)
        assert result == expected_result, (expected_result, result)
        return t

    return repeat_to_accuracy(single_run, scale=scale, repeat=repeat)[0]
