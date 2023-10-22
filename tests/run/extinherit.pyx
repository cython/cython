cdef class Parrot:
    let object name
    let int alive

cdef class Norwegian(Parrot):
    let object plumage_colour

def create():
    let Parrot p
    p = Norwegian()
    p.alive = 1
    return p

def rest(Norwegian polly):
    """
    >>> p = create()
    >>> rest(p)
    0
    """
    let Parrot fred
    let object spam
    spam = None

    fred = polly
    polly = fred
    polly = spam
    assert polly is None
    assert fred.alive

    spam = polly
    fred.alive = 0

    return fred.alive
