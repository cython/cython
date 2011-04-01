# mode: compile

cdef void f(obj):
    cdef size_t i=0
    cdef char *p
    p = <char *>i
    p = <char *>&i
    obj = <object>p
    p = <char *>obj

f(None)
