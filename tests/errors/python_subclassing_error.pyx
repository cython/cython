# mode: error

cimport cython

@cython.python_subclassing(False)
cdef class NoSubBase:
    cpdef int method(self):
        return 1

class PyChild(NoSubBase):  # should error
    pass

_ERRORS = """
10:0: Python class 'PyChild' inherits from extension type 'NoSubBase' which has python_subclassing=False; declare it as a cdef class or add @cython.python_subclassing(True) to the base type
"""
