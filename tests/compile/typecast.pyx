# mode: compile

cdef void f(obj):
    let size_t i=0
    let char *p
    p = <char *>i
    p = <char *>&i
    obj = <object>p
    p = <char *>obj

f(None)
