from __future__ import print_function
cimport cython

ctypedef fused char_or_float:
    cython.char
    cython.float


cpdef char_or_float plus_one(char_or_float var):
    return var + 1


def show_me():
    cdef:
        cython.char a = 127
        cython.float b = 127
    print('char', plus_one(a))
    print('float', plus_one(b))
