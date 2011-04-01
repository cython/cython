# mode: compile

cdef int grail():
    cdef int (*spam)()
    spam = &grail
    spam = grail
    spam()

ctypedef int funcptr_t()

cdef inline funcptr_t* dummy():
    return &grail
