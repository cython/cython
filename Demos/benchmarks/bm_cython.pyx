import cython

import array
import collections
import time


def _unpack_buffer_const_char_1d(provider, number, timer=time.perf_counter):
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


def _with_contextmanager_pass(cm, number, timer=time.perf_counter):
    t = timer()
    for _ in range(number):
        with cm:
            pass
    t = timer() - t
    return t


def _with_contextmanager_raise(cm, number, timer=time.perf_counter):
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
