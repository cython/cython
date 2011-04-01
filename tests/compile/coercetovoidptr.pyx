# mode: compile

cdef void f():
    cdef void *p
    cdef char *q=NULL
    p = q

f()
