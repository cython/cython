__doc__ = """
    >>> h()
    (1, b'test', 3, 1, b'test', 3)
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")

def f():
    """
    >>> f()
    (1, 2, 1, 2)
    """
    cdef object obj1a, obj2a, obj3a, obj1b, obj2b, obj3b
    obj1b, obj2b, obj3b = 1, 2, 3
    obj1a, obj2a = obj1b, obj2b
    return obj1a, obj2a, obj1b, obj2b

def g():
    """
    >>> g()
    (1, 1, 2, 2, 3, 3)
    """
    cdef object obj1a, obj2a, obj3a, obj1b, obj2b, obj3b
    obj1b, obj2b, obj3b = 1, 2, 3
    obj1a, [obj2a, obj3a] = [obj1b, (obj2b, obj3b)]
    return obj1a, obj1b, obj2a, obj2b, obj3a, obj3b

def h():
    cdef object obj1a, obj2a, obj3a, obj1b, obj2b, obj3b
    cdef int int1, int2
    cdef char *ptr1, *ptr2
    int2, ptr2, obj1b = 1, "test", 3
    int1, ptr1, obj1a = int2, ptr2, obj1b
    return int1, ptr1, obj1a, int2, ptr2, obj1b

def j():
    """
    >>> j()
    (2, 1, 4, 2, 6, 3)
    """
    cdef object obj1a, obj2a, obj3a, obj1b, obj2b, obj3b
    obj1b, obj2b, obj3b = 1, 2, 3
    obj1a, obj2a, obj3a = obj1b + 1, obj2b + 2, obj3b + 3
    return obj1a, obj1b, obj2a, obj2b, obj3a, obj3b
