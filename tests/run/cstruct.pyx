cdef struct Grail

cdef struct Spam:
    int i
    char c
    float *p[42]
    Grail *g

cdef struct Grail:
    Spam *s

cdef Spam spam, ham

cdef void eggs(Spam s):
    cdef int j
    j = s.i
    s.i = j

spam = ham
