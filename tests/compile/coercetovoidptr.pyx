# mode: compile

cdef void f():
    cdef void *p
    cdef i8 *q=NULL
    p = q

f()
