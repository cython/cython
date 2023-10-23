cdef extern from "foo.h":
    ctypedef i128 big_t
    fn void spam(big_t b)

spam(grail)
