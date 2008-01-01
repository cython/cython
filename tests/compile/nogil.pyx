cdef extern object g(int x) nogil

cdef void f(int x) nogil:
    cdef int y
    y = 42
