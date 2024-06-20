# mode: error

import math

cdef double cfunc(double x) except math.nan:
    return x


_ERRORS = """
5:39: Exception value must be constant
5:39: Not allowed in a constant expression
"""
