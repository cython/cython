# tag: numpy
cimport cython


@cython.ufunc
cdef cython.numeric generic_add_one(cython.numeric x):
    return x+1
