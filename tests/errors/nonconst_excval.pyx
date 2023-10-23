# mode: error

import math

fn f64 cfunc(f64 x) except math.nan:
    return x


_ERRORS = """
5:31: Exception value must be constant
5:31: Not allowed in a constant expression
"""
