# mode: error

def f():
    cdef (int, int) t = (1, 2)
    return <(int, int, int)>t

_ERRORS = u"""
5:11: Cannot cast '(int, int)' to '(int, int, int)'
"""
