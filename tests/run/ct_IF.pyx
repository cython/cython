__doc__ = u"""
    >>> f()
    1
    >>> g()
    2
    >>> h()
    3
"""

DEF NO = 0
DEF YES = 1

def f():
    cdef int i
    IF YES:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3
    return i

def g():
    cdef int i
    IF NO:
        i = 1
    ELIF YES:
        i = 2
    ELSE:
        i = 3
    return i

def h():
    cdef int i
    IF NO:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3
    return i
