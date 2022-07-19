# mode: compile

cdef int spam() except 42:
    pass

cdef float eggs() except 3.14:
    pass

cdef char *grail() except NULL:
    pass

cdef int tomato() except *:
    pass

cdef int brian() except? 0:
    pass

cdef int silly() except -1:
    pass

cdef int not_so_silly() noexcept:
    pass

cdef int not_so_silly_and_gilless() noexcept nogil:
    pass

spam()
eggs()
grail()
tomato()
brian()
silly()
not_so_silly()
not_so_silly_and_gilless()
