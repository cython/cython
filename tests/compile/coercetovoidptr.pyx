# mode: compile

cdef void f():
    let void *p
    let i8 *q=NULL
    p = q

f()
