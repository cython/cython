cdef class Parrot:
    cdef object name
    cdef int alive

cdef class Norwegian(Parrot):
    cdef object plumage_colour

cdef void rest(Norwegian polly):
    cdef Parrot fred
    cdef object spam
    fred = polly
    polly = fred
    polly = spam
    spam = polly
    polly.alive = 0
