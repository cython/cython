import cython

import time


builtin_collections = cython.fused_type(
    list,
    tuple,
    set,
    dict,
    object,
)

# FIXME: This should work but currently fails to define a fused type alias name:
# builtin_collections2 = cython.typedef(builtin_collections)
# builtin_collections3 = cython.typedef(builtin_collections)

builtin_collections2 = cython.fused_type(
    list,
    tuple,
    set,
    dict,
    object,
)

builtin_collections3 = cython.fused_type(
    list,
    tuple,
    set,
    dict,
    object,
)


def _fused_func_args_1(o: builtin_collections):
    assert o is not None


def _call_fused_func_args_1(number: cython.int, timer):
    func = _fused_func_args_1
    args = [[], (), set(), {}, 5]
    number = max(1, number // len(args))

    t = timer()
    for _ in range(number):
        for arg in args:
            func(arg)
    t = timer() - t
    return t


def _fused_func_args_2(o1: builtin_collections, o2: builtin_collections2):
    assert o1 is not None
    assert o2 is not None


def _call_fused_func_args_2(number: cython.int, timer):
    func = _fused_func_args_2
    args = [[], (), set(), {}, 5]
    number = max(1, number // (len(args) ** 2))

    t = timer()
    for _ in range(number):
        for arg1 in args:
            for arg2 in args:
                func(arg1, arg2)
    t = timer() - t
    return t


def _fused_func_args_3(o1: builtin_collections, o2: builtin_collections2, o3: builtin_collections3):
    assert o1 is not None
    assert o2 is not None
    assert o3 is not None


def _call_fused_func_args_3(number: cython.int, timer):
    func = _fused_func_args_3
    args = [[], (), set(), {}, 5]
    number = max(1, number // (len(args) ** 3))

    t = timer()
    for _ in range(number):
        for arg1 in args:
            for arg2 in args:
                for arg3 in args:
                    func(arg1, arg2, arg3)
    t = timer() - t
    return t


def get_benchmarks():
    return {
        'fused_args_1': _call_fused_func_args_1,
        'fused_args_2': _call_fused_func_args_2,
        'fused_args_3': _call_fused_func_args_3,
    }


def run_benchmark(repeat=True, scale=100):
    from util import repeat_to_accuracy, scale_subbenchmarks

    benchmarks = get_benchmarks()

    timings = {
        name: func(1000, time.perf_counter)
        for name, func in benchmarks.items()
    }
    scales = scale_subbenchmarks(timings, scale)

    collected_timings = {}

    for name, func in benchmarks.items():
        collected_timings[name] = repeat_to_accuracy(
            func, scale=scales[name], repeat=repeat)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
