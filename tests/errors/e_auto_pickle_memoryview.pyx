# mode: error
# tag: memoryview
# ticket: 6767

cimport cython


@cython.auto_pickle(True)
cdef class TestClass:
    cdef double[:, :] x


_ERRORS = """
8:0: self.x cannot be pickled because typed memoryviews are not pickleable
"""
