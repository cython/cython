# mode: error

# Python import (not cimport) of a cdef class with python_subclassing=False.
# The compile-time check should still fire via pxd fallback lookup.

from python_subclassing_pyimport_base import Base

class PyChild(Base):  # should error
    pass

_ERRORS = """
8:0: Python class 'PyChild' inherits from extension type 'Base' which has python_subclassing=False; declare it as a cdef class or add @cython.python_subclassing(True) to the base type
"""
