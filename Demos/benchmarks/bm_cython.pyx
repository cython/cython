import cython

import array
import collections
import time

from functools import partial


# Memoryviews.

def _unpack_buffer_const_char_1d(provider, int number, timer=time.perf_counter):
    cdef const unsigned char[:] buffer

    t = timer()
    for _ in range(number):
        buffer = provider
    t = timer() - t
    return t


_bytes_data = bytes(1000)
bm_mview_const_char_bytes = partial(_unpack_buffer_const_char_1d, _bytes_data)
bm_mview_const_char_bytearray = partial(_unpack_buffer_const_char_1d, bytearray(_bytes_data))
bm_mview_const_char_pyarray = partial(_unpack_buffer_const_char_1d, array.array('B', _bytes_data))
del _bytes_data


cdef const unsigned char[:] _pass_slice(const unsigned char[:] view):
    return view[::2]


def _slice_memoryview(data, int number, timer=time.perf_counter):
    cdef const unsigned char[:] view = data
    cdef const unsigned char[:] view2
    cdef long dummy = 0
    cdef Py_ssize_t i

    t = timer()

    for _ in range(number):
        for i in range(len(view) - 1):
            view2 = _pass_slice(view[i:])
            dummy += view2[0]

            view2 = _pass_slice(view[:i+1])
            dummy -= view2[i // 2]

    t = timer() - t

    if dummy == 0:
        raise RuntimeError("did it calculate?")
    return t


bm_slice_memoryview = partial(_slice_memoryview, bytes([i % 256 for i in range(100)]))


# With statement.

def _with_contextmanager_pass(cm, int number, timer=time.perf_counter):
    i: cython.long
    t = timer()
    for i in range(number):
        with cm:
            pass
    t = timer() - t
    return t


def _with_contextmanager_raise(cm, int number, timer=time.perf_counter):
    i: cython.long
    exception = TypeError()
    t = timer()
    for i in range(number):
        with cm:
            raise exception
    t = timer() - t
    return t


class PyCM:
    def __enter__(self): pass
    def __exit__(self, ex1, ex2, ex3): return True


cdef class CyCM:
    def __enter__(self): pass
    def __exit__(self, ex1, ex2, ex3): return True


bm_with_PyCM_pass = partial(_with_contextmanager_pass, PyCM())
bm_with_CyCM_pass = partial(_with_contextmanager_pass, CyCM())
bm_with_PyCM_raise = partial(_with_contextmanager_raise, PyCM())
bm_with_CyCM_raise = partial(_with_contextmanager_raise, CyCM())


# Create inner functions.

def bm_create_inner_func_plain(scale, timer=time.perf_counter):
    i: cython.long
    t = timer()
    for i in range(scale):
        def inner_a(arg1, int arg2):
            pass
        def inner_b(arg1, int arg2):
            pass
        def inner_c(arg1, int arg2):
            pass
    t = timer() - t
    return t


def bm_create_inner_func_closure(scale, timer=time.perf_counter):
    i: cython.long
    t = timer()
    for i in range(scale):
        def inner1():
            pass
        def inner2(arg1, int arg2):
            return inner1()
        def inner3(arg1, arg2=inner1):
            return inner2()
    t = timer() - t
    return t


# Iterate over first digits of π.

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
    any_none: bool = False
    t = timer()
    for i in range(scale):
        for ch in (
                "3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                "2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    t = timer() - t
    assert not any_none
    return t


def bm_iter_bytes_listcomp(scale, timer=time.perf_counter):
    t = timer()
    for i in range(scale):
        [ch for ch in (
            b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
            b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
        )]
    t = timer() - t
    return t


def bm_iter_bytes_forin(scale, timer=time.perf_counter):
    any_none: bool = False
    t = timer()
    for i in range(scale):
        for ch in (
                b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    t = timer() - t
    assert not any_none
    return t


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
