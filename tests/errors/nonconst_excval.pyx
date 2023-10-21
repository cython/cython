# mode: error

import math

cdef f64 cfunc(f64 x) except math.nan:
    return x


_ERRORS = """
5:33: Exception value must be constant
5:33: Not allowed in a constant expression
"""
