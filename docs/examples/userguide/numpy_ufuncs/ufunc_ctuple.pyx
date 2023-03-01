# tag: numpy
cimport cython


@cython.ufunc
cdef (int, int) add_one_add_two(int x):
    return x+1, x+2
