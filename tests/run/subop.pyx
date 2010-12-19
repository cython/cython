def f():
    """
    >>> f()
    (-1, -1)
    """
    cdef int int1, int2, int3
    obj1 = 1
    obj2 = 2
    obj3 = 3
    int2 = 2
    int3 = 3

    int1 = int2 - int3
    obj1 = obj2 - int3
    return int1, obj1

def p():
    """
    >>> p()
    0
    """
    cdef int int1, int2, int3
    cdef char *ptr1, *ptr2, *ptr3
    int2 = 2
    int3 = 3
    ptr2 = "test"
    ptr3 = ptr2

    ptr1 = ptr2 - int3
    int1 = ptr2 - ptr3
    return int1
