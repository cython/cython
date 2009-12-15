cdef class Parrot:
    cdef object name
    cdef int alive

cdef class Norwegian(Parrot):
    cdef object plumage_colour

def create():
    cdef Parrot p
    p = Norwegian()
    p.alive = 1
    return p

def rest(Norwegian polly):
    """
    >>> p = create()
    >>> rest(p)
    0
    """
    cdef Parrot fred
    cdef object spam
    spam = None

    fred = polly
    polly = fred
    polly = spam
    assert polly is None
    assert fred.alive

    spam = polly
    fred.alive = 0

    return fred.alive
