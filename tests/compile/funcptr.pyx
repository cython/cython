cdef int grail():
    cdef int (*spam)()
    spam = &grail
    spam = grail
    spam()

