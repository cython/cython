cdef object f(object x):
    cdef int y
    #z = 42
    with nogil:
        pass#y = 17
    #z = 88

cdef object g():
    with nogil:
        h()

cdef int h() except -1:
    pass
