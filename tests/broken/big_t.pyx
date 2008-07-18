cdef extern from "foo.h":
    ctypedef long long big_t
    cdef void spam(big_t b)

spam(grail)
