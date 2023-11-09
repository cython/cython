# mode: run
# tag: warnings

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


_IGNORE = """
4:0: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
5:0: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
57:8: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
60:8: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
72:8: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
75:8: The 'DEF' statement is deprecated and will be removed in a future Cython version. Consider using global variables, constants, and in-place literals instead. See https://github.com/cython/cython/issues/4310
"""

_WARNINGS = """
13:4: The 'IF' statement is deprecated and will be removed in a future Cython version. Consider using runtime conditions or C macros instead. See https://github.com/cython/cython/issues/4310
27:4: The 'IF' statement is deprecated and will be removed in a future Cython version. Consider using runtime conditions or C macros instead. See https://github.com/cython/cython/issues/4310
41:4: The 'IF' statement is deprecated and will be removed in a future Cython version. Consider using runtime conditions or C macros instead. See https://github.com/cython/cython/issues/4310
56:4: The 'IF' statement is deprecated and will be removed in a future Cython version. Consider using runtime conditions or C macros instead. See https://github.com/cython/cython/issues/4310
71:4: The 'IF' statement is deprecated and will be removed in a future Cython version. Consider using runtime conditions or C macros instead. See https://github.com/cython/cython/issues/4310
"""
