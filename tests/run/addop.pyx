def f():
    """
    >>> f()
    (30, 22)
    """
    cdef int int1, int2, int3
    cdef char *ptr1, *ptr2 = "test", *ptr3 = "toast"
    int2 = 10
    int3 = 20
    obj1 = 1
    obj2 = 2
    obj3 = 3
    int1 = int2 + int3
    ptr1 = ptr2 + int3
    ptr1 = int2 + ptr3
    obj1 = obj2 + int3
    return int1, obj1
