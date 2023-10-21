cdef extern from "foo.h":
    ctypedef i128 big_t
    cdef void spam(big_t b)

spam(grail)
