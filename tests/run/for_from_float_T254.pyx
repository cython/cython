# ticket: t254

def double_target(a, b):
    """
    >>> double_target(0, 4)
    at 0.0
    at 1.0
    at 2.0
    at 3.0
    4.0
    """
    cdef double x
    for x from a <= x < b:
        print u"at", x
    return x

def double_step(a, b, dx):
    """
    >>> double_step(0, 2, .5)
    at 0.0
    at 0.5
    at 1.0
    at 1.5
    2.0
    """
    cdef double x
    for x from a <= x < b by dx:
        print u"at", x
    return x

def double_step_typed(a, b, double dx):
    """
    >>> double_step_typed(0, 2, .5)
    at 0.0
    at 0.5
    at 1.0
    at 1.5
    2.0
    """
    cdef double x
    for x from a <= x < b by dx:
        print u"at", x
    return x

def double_step_py_target(a, b, double dx):
    """
    >>> double_step_py_target(0, 2, .5)
    at 0.0
    at 0.5
    at 1.0
    at 1.5
    2.0
    """
    cdef object x
    for x from a <= x < b by dx:
        print u"at", x
    return x

def int_step_py_target(a, b, int dx):
    """
    >>> int_step_py_target(0, 2, 1)
    at 0
    at 1
    2
    """
    cdef object x
    for x from a <= x < b by dx:
        print u"at", x
    return x
