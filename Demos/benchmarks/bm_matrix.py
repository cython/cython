import collections
import time
from functools import partial

import cython

DEFAULT_TIMER = time.perf_counter
MATRIX_SIZE = 40

MATRIX = [[2.] * MATRIX_SIZE for i in range(MATRIX_SIZE)]


def _multiply_matrices(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t
    result: float

    for i in range(size):
        for j in range(size):
            result = 0.
            for k in range(size):
                result += A[i][k] * B[k][j]
            C[i][j] = result


def _multiply_matrices_2d(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t
    result: float

    for i in range(size):
        for j in range(size):
            result = 0.
            for k in range(size):
                result += A[i,k] * B[k,j]
            C[i,j] = result


def _bm_matrix(mkarray, bm_func, iterations: cython.Py_ssize_t, timer=DEFAULT_TIMER):
    A = mkarray(MATRIX)
    B = mkarray(MATRIX)
    C = mkarray(MATRIX)

    i: cython.Py_ssize_t
    t = timer()
    for i in range(iterations):
        bm_func(A, B, C)
    t = timer() - t
    return t


def _list_matrix(matrix):
    return [row[:] for row in matrix]

def _array_matrix(matrix):
    from array import array
    return [array('d', row) for row in matrix]

def _numpy_matrix(matrix):
    from numpy import asarray
    return asarray(matrix)

def _memview_matrix(matrix):
    view: cython.double[:,:] = _numpy_matrix(matrix)
    return view


bm_matrix_list = partial(_bm_matrix, _list_matrix, _multiply_matrices)
bm_matrix_array = partial(_bm_matrix, _array_matrix, _multiply_matrices)
bm_matrix_numpy = partial(_bm_matrix, _numpy_matrix, _multiply_matrices)
bm_matrix_numpy_memview = partial(_bm_matrix, _memview_matrix, _multiply_matrices)

bm_matrix_numpy_2d = partial(_bm_matrix, _numpy_matrix, _multiply_matrices_2d)
bm_matrix_numpy_memview_2d = partial(_bm_matrix, _memview_matrix, _multiply_matrices_2d)


# main

def run_benchmark(repeat=True, scale=5):
    from util import repeat_to_accuracy, scale_subbenchmarks

    benchmarks = [
        (name, func)
        for name, func in globals().items()
        if name.startswith('bm_')
    ]

    try:
        import numpy
    except ImportError:
        benchmarks = [
            (name, func)
            for name, func in benchmarks
            if 'numpy' not in name
        ]

    collected_timings = collections.defaultdict(list)

    timings = {}
    for name, func in benchmarks:
        if name.startswith('bm_'):
            timings[name] = func(3)

    scales = scale_subbenchmarks(timings, scale)

    for name, func in benchmarks:
        if name.startswith('bm_'):
            collected_timings[name] = repeat_to_accuracy(
                func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
