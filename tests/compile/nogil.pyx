cdef extern object g(object x) nogil

cdef void f(int x) nogil:
    cdef int y
    y = 42
