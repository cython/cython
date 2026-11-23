# mode: error
# tag: fused

cimport cython


cdef class A:
    def __cinit__(self, cython.integral val):
        pass

    def __getitem__(self, cython.integral idx):
        return idx

_ERRORS = """
8:4: Fused types are not supported in special methods
11:4: Fused types are not supported in special methods
"""
