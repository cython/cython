cdef extern void spam(char *s)

cdef struct Grail:
    char silly[42]

cdef void eggs():
    cdef char silly[42]
    cdef Grail grail
    spam(silly)
    spam(grail.silly)

eggs()
