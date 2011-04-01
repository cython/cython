# mode: compile

cdef enum Spam:
    a
    b, c,
    d, e, f
    g = 42

cdef void eggs():
    cdef Spam s1, s2=a
    cdef int i
    s1 = s2
    s1 = c
    i = s1

eggs()
