# mode: compile

cdef extern object g(object x) nogil
cdef extern void g2(object x) nogil

cdef extern from "nogil.h":
        void e1() nogil
        i32 *e2() nogil

fn void f(i32 x) nogil:
        cdef i32 y
        y = 42

fn void h(object x) nogil:
        cdef void *p=<void*>None
        g2(x)
        g2(<object>p)
        p = <void *>x
        e1()
        e2()

f(0)
h(None)
