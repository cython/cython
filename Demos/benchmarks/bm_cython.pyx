import cython

import array
import collections
import time


def _unpack_buffer_const_char_1d(provider, int number, timer=time.perf_counter):
    cdef const unsigned char[:] buffer

    t = timer()
    for _ in range(number):
        buffer = provider
    t = timer() - t
    return t


def bm_unpack_buffer_const_char_1d(number, timer=time.perf_counter):
    data = bytes(1000)
    #cdef const unsigned char[:] memview = data
    return {
        'unpack_buffer[const char 1d, bytes]': _unpack_buffer_const_char_1d(data, number, timer),
        'unpack_buffer[const char 1d, bytearray]': _unpack_buffer_const_char_1d(bytearray(data), number, timer),
        'unpack_buffer[const char 1d, array]': _unpack_buffer_const_char_1d(array.array('B', data), number, timer),
        #'unpack_buffer[const char 1d, cymemview]': _unpack_buffer_const_char_1d(memview, number, timer),
    }


def _with_contextmanager_pass(cm, int number, timer=time.perf_counter):
    t = timer()
    for _ in range(number):
        with cm:
            pass
    t = timer() - t
    return t


def _with_contextmanager_raise(cm, int number, timer=time.perf_counter):
    exception = TypeError()
    t = timer()
    for _ in range(number):
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


def bm_with_statement(number, timer=time.perf_counter):
    return {
        'with_pass_PyCM': _with_contextmanager_pass(PyCM(), number, timer),
        'with_pass_CyCM': _with_contextmanager_pass(CyCM(), number, timer),
        'with_raise_PyCM': _with_contextmanager_raise(PyCM(), number, timer),
        'with_raise_CyCM': _with_contextmanager_raise(CyCM(), number, timer),
    }


def bm_create_inner_function(int number, timer=time.perf_counter):
    t = timer()
    for _ in range(number):
        def inner_a(arg1, int arg2):
            pass
        def inner_b(arg1, int arg2):
            pass
        def inner_c(arg1, int arg2):
            pass
    plain_time = timer() - t

    t = timer()
    for _ in range(number):
        def inner1():
            pass
        def inner2(arg1, int arg2):
            return inner1()
        def inner3(arg1, arg2=inner1):
            return inner2()
    closure_time = timer() - t

    return {
        'create_inner_function[plain]': plain_time,
        'create_inner_function[closure]': closure_time,
    }


def bm_iter_string_literal(int number, timer=time.perf_counter):
    # iterate over first digits of π
    any_none: bool

    # str
    t = timer()
    for _ in range(number):
        [ch for ch in (
            "3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
            "2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
        )]

    any_none = False
    for _ in range(number):
        for ch in (
                "3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                "2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    str_time = timer() - t
    assert not any_none

    # bytes
    t = timer()
    for _ in range(number):
        [ch for ch in (
            b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
            b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
        )]

    any_none = False
    for _ in range(number):
        for ch in (
                b"3141592653589793238462643383279502884197169399375105820974944592307816406286"  # 76 characters
                b"2089986280348253421170679821480865132823066470938446095505822317253594081284"  # 76 characters
                ):
            any_none |= (ch is None)
    bytes_time = timer() - t
    assert not any_none

    return {
        'iter_str': str_time,
        'iter_bytes': bytes_time,
    }


def run_benchmark(repeat: cython.int = 10, number=100, timer=time.perf_counter):
    i: cython.int

    collected_timings = collections.defaultdict(list)

    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue

        for i in range(repeat):
            timings = func(number, timer)
            for name, t in timings.items():
                collected_timings[name].append(t)

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
