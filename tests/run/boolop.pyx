__doc__ = u"""
    >>> foo(True, False, 23, 'test', 1)
    (0, 1, False, False)
"""

def foo(obj1, obj2, obj3, obj4, obj5):
    cdef int bool1, bool2, bool3, bool4
    cdef char *ptr
    cdef float f
    bool1 = 1
    bool2 = 0
    ptr = NULL
    f = 0.0

    bool3 = bool1 and bool2
    bool3 = bool1 or bool2
    bool3 = obj1 and obj2
    bool3 = bool1 and ptr
    bool3 = bool1 and f
    bool4 = bool1 and bool2 and bool3
    bool4 = bool1 or bool2 and bool3
    obj4 = obj1 and obj2 and obj3
    obj5 = (obj1 + obj2 + obj3) and obj4
    return bool3, bool4, obj4, obj5
