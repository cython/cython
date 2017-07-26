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


def control_flow_DEF1():
    """
    >>> control_flow_DEF1()
    B should be 2.
    2
    """
    IF YES:
        DEF B=2
        print('B should be 2.')
    ELSE:
        DEF B=3
        print('B should be 3.')
    return B


def control_flow_DEF2():
    """
    >>> control_flow_DEF2()
    B should be 3.
    3
    """
    IF NO:
        DEF B=2
        print('B should be 2.')
    ELSE:
        DEF B=3
        print('B should be 3.')
    return B
