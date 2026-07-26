# cython: auto_pickle=False

import cython

import collections
import time


### Iterate over first digits of π, stored as a C array.

def bm_iter_str_listcomp(scale, timer=time.perf_counter):
    i: cython.long
    t = timer()
    for i in range(scale):
        [ch for ch in (
            "3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
            "2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
        )]
    t = timer() - t
    return t


def bm_iter_str_forin(scale, timer=time.perf_counter):
    i: cython.long
    any_none: bool = False
    t = timer()
    for i in range(scale):
        for ch in (
                "3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                "2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    t = timer() - t
    if any_none:
        raise RuntimeError("unexpected result")
    return t


def bm_iter_bytes_listcomp(scale, timer=time.perf_counter):
    i: cython.long
    t = timer()
    for i in range(scale):
        [ch for ch in (
            b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
            b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
        )]
    t = timer() - t
    return t


def bm_iter_bytes_forin(scale, timer=time.perf_counter):
    i: cython.long
    any_none: bool = False
    t = timer()
    for i in range(scale):
        for ch in (
                b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    t = timer() - t
    if any_none:
        raise RuntimeError("unexpected result")
    return t


#### main ####

def time_benchmarks(scale):
    timings = {}
    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        timings[name] = func(scale)
    return timings


def run_benchmark(repeat: bool, scale=1000):
    from util import repeat_to_accuracy, scale_subbenchmarks

    scales = scale_subbenchmarks(time_benchmarks(1000), scale)

    collected_timings = collections.defaultdict(list)

    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        collected_timings[name] = repeat_to_accuracy(func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
