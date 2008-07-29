cdef void f(obj):
    cdef int i
    cdef char *p
    p = <char *>i
    obj = <object>p
    p = <char *>obj
    