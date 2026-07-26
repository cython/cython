from __future__ import annotations

import collections
import time
from functools import partial

import cython

if cython.compiled:
    from cython.cimports.libc.stdint import int64_t

DEFAULT_TIMER = time.perf_counter
MATRIX_SIZE = 40

FLOAT_MATRIX = [[2.] * MATRIX_SIZE for i in range(MATRIX_SIZE)]
INT_MATRIX = [[2] * MATRIX_SIZE for i in range(MATRIX_SIZE)]


def _multiply_matrices_float(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t

    for i in range(size):
        for j in range(size):
            result = 0.
            for k in range(size):
                result += A[i][k] * B[k][j]
            C[i][j] = result


def _multiply_matrices_int(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t

    for i in range(size):
        for j in range(size):
            result = 0
            for k in range(size):
                result += A[i][k] * B[k][j]
            C[i][j] = result


def _multiply_matrices_2d_float(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t

    for i in range(size):
        for j in range(size):
            result = 0.
            for k in range(size):
                result += A[i,k] * B[k,j]
            C[i,j] = result


def _multiply_matrices_2d_int(A, B, C):
    size: cython.Py_ssize_t = len(A)
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    k: cython.Py_ssize_t

    for i in range(size):
        for j in range(size):
            result = 0
            for k in range(size):
                result += A[i,k] * B[k,j]
            C[i,j] = result


def _bm_matrix(mkarray, matrix, bm_func, iterations: cython.Py_ssize_t, timer=DEFAULT_TIMER):
    A = mkarray(matrix)
    B = mkarray(matrix)
    C = mkarray(matrix)

    i: cython.Py_ssize_t
    t = timer()
    for i in range(iterations):
        bm_func(A, B, C)
    t = timer() - t
    return t


def _list_matrix(matrix):
    return [row[:] for row in matrix]

def _list_matrix_mix(matrix):
    tp = [float, int, int, float, float, float, int, int]
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t

    return [
        [tp[(i*j) % 8](cell) for j, cell in enumerate(row)]
        for i, row in enumerate(matrix)
    ]

def _array_matrix_float(matrix):
    from array import array
    return [array('d', row) for row in matrix]

def _array_matrix_int(matrix):
    from array import array
    return [array('i', row) for row in matrix]

def _numpy_matrix_float(matrix):
    from numpy import asarray, float64
    return asarray(matrix, dtype=float64)

def _numpy_matrix_int(matrix):
    from numpy import asarray, int64
    return asarray(matrix, dtype=int64)

def _memview_matrix_float(matrix):
    view: cython.double[:,:] = _numpy_matrix_float(matrix)
    return view

def _memview_matrix_int(matrix):
    view: int64_t[:,:] = _numpy_matrix_int(matrix)
    return view


bm_matrix_list_float = partial(_bm_matrix, _list_matrix, FLOAT_MATRIX, _multiply_matrices_float)
bm_matrix_array_float = partial(_bm_matrix, _array_matrix_float, FLOAT_MATRIX, _multiply_matrices_float)
bm_matrix_numpy_float = partial(_bm_matrix, _numpy_matrix_float, FLOAT_MATRIX, _multiply_matrices_float)
bm_matrix_numpy_memview_float = partial(_bm_matrix, _memview_matrix_float, FLOAT_MATRIX, _multiply_matrices_float)

bm_matrix_numpy_2d_float = partial(_bm_matrix, _numpy_matrix_float, FLOAT_MATRIX, _multiply_matrices_2d_float)
bm_matrix_numpy_memview_2d_float = partial(_bm_matrix, _memview_matrix_float, FLOAT_MATRIX, _multiply_matrices_2d_float)

bm_matrix_list_int = partial(_bm_matrix, _list_matrix, INT_MATRIX, _multiply_matrices_int)
bm_matrix_array_int = partial(_bm_matrix, _array_matrix_int, INT_MATRIX, _multiply_matrices_int)
bm_matrix_numpy_int = partial(_bm_matrix, _numpy_matrix_int, INT_MATRIX, _multiply_matrices_int)
bm_matrix_numpy_memview_int = partial(_bm_matrix, _memview_matrix_int, INT_MATRIX, _multiply_matrices_int)

bm_matrix_numpy_2d_int = partial(_bm_matrix, _numpy_matrix_int, INT_MATRIX, _multiply_matrices_2d_int)
bm_matrix_numpy_memview_2d_int = partial(_bm_matrix, _memview_matrix_int, INT_MATRIX, _multiply_matrices_2d_int)

bm_matrix_list_mix = partial(_bm_matrix, _list_matrix_mix, INT_MATRIX, _multiply_matrices_int)


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
