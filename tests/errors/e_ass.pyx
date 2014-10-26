# mode: error

cdef void foo(obj):
    cdef int i1
    cdef char *p1
    cdef int *p2
    i1 = p1 # error
    p2 = obj # error

    obj = p2 # error


_ERRORS = u"""
7:19: Cannot assign type 'char *' to 'int'
8:20: Cannot convert Python object to 'int *'
10:20: Cannot convert 'int *' to Python object
"""
