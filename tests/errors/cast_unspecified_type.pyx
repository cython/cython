# mode: error
# ticket: 7683

import cython

def f():
    s = ""
    y: cython.typeof(s)
    b = cython.cast(cython.typeof(y), s)


_ERRORS = u"""
9:14: Unable to determine the type to cast to
"""
