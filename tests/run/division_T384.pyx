# ticket: t384

"""
>>> test(3)
(3+1j)
"""

cimport cython

ctypedef isize index_t

ctypedef double complex mycomplex

ctypedef struct MyStruct:
    mycomplex a, b

@cython.cdivision(false)
def test(index_t x):
    cdef index_t y = x // 2
    cdef MyStruct s
    s.a = x + y*1j
    return s.a
