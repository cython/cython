cdef void f(obj):
    cdef int i=0
    cdef char *p
    p = <char *>i
    obj = <object>p
    p = <char *>obj

f(None)
