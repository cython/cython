cdef void f():
    cdef object obj1a, obj2a, obj3a, obj1b, obj2b, obj3b
    cdef int int1, int2
    cdef char *ptr1, *ptr2
    obj1a, obj2a = obj1b, obj2b
    obj1a, [obj2a, obj3a] = [obj1b, (obj2b, obj3b)]
    int1, ptr1, obj1a = int2, ptr2, obj1b
    obj1a, obj2a, obj3a = obj1b + 1, obj2b + 2, obj3b + 3
