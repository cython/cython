# mode: error

cimport cython


@cython.python_subclassing(False)
cdef class A:
    cpdef int m(self):
        return 1


@cython.python_subclassing(True)
cdef class B(A):
    pass


@cython.python_subclassing(False)
cdef class C(B):
    pass


_ERRORS = """
17:0: cannot disable python_subclassing on 'C': an ancestor class has it locked to True
"""
