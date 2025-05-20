# mode: compile
# tag: warnings

# These should compile (because they used to compile) but have never been a sensible thing to do.

from libc.math cimport NAN

cdef double f1() except NAN:
    return 0

DEF FLOAT_ERROR = float("nan")

cdef double f2() except FLOAT_ERROR:
    return 1

_WARNINGS = """
6:24: 'NAN' is most likely unsuitable for use as an exception value because it cannot be compared with the '==' operator
11:24: 'nan' is unsuitable for use as an exception value because it cannot be compared with the '==' operator
"""
