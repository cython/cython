"""
Test for memory leaks when adding more memory view attributes in subtypes.
"""

import gc

from cython.view cimport array


def count_memoryviews():
    gc.collect()
    return sum([1 if 'memoryview' in str(type(o)) else 0
                for o in gc.get_objects()])


def run_test(cls, num_iters):
    orig_count = count_memoryviews()
    def f():
        x = cls(1024)
    for i in range(num_iters):
        f()
    return count_memoryviews() - orig_count


cdef class BaseType:
    """
    >>> run_test(BaseType, 10)
    0
    """
    cdef double[:] buffer

    def __cinit__(self, n):
        self.buffer = array((n,), sizeof(double), 'd')


cdef class Subtype(BaseType):
    """
    >>> run_test(Subtype, 10)
    0
    """
    cdef double[:] buffer2

    def __cinit__(self, n):
        self.buffer2 = array((n,), sizeof(double), 'd')


cdef class SubtypeWithUserDealloc(BaseType):
    """
    >>> run_test(SubtypeWithUserDealloc, 10)
    0
    """
    cdef double[:] buffer2

    def __cinit__(self, n):
        self.buffer2 = array((n,), sizeof(double), 'd')

    def __dealloc__(self):
        pass
