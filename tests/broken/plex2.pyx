cdef class Spam:
    pass

cdef void foo(object blarg):
    pass

cdef void xyzzy():
    cdef Spam spam
    foo(spam)
