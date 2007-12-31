cdef union Spam:
    int i
    char c
    float *p[42]

cdef Spam spam, ham

cdef void eggs(Spam s):
    cdef int j
    j = s.i
    s.i = j

spam = ham
