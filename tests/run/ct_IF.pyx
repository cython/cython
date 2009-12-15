DEF NO = 0
DEF YES = 1

def f():
    """
    >>> f()
    1
    """
    cdef int i
    IF YES:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3
    return i

def g():
    """
    >>> g()
    2
    """
    cdef int i
    IF NO:
        i = 1
    ELIF YES:
        i = 2
    ELSE:
        i = 3
    return i

def h():
    """
    >>> h()
    3
    """
    cdef int i
    IF NO:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3
    return i
