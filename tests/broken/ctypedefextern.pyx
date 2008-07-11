cdef extern from "ctypedefextern.h":

    ctypedef int some_int
    ctypedef some_int *some_ptr

cdef void spam():
    cdef some_int i
    cdef some_ptr p
    p[0] = i
