# mode: compile
# tag: cpp


cpdef enumclass Spam:
    a
    b
    c
    d
    e
    f = 42

cdef void eggs():
    cdef Spam s1
    s1 = Spam.a
    s2 = Spam.b

eggs()
