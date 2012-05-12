cdef class A:
    """
    >>> a = A(3); a
    A(3)
    >>> import cPickle
    >>> cPickle.loads(cPickle.dumps(a))
    A(3)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    A(3)
    """

    cdef int value

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "A(%s)" % self.value

    def __reduce__(self):
        return A, (self.value,)

cdef class B:
    """
    >>> b = B(x=37, y=389); b
    B(x=37, y=389)
    >>> import cPickle
    >>> cPickle.loads(cPickle.dumps(b))
    B(x=37, y=389)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(b))
    B(x=37, y=389)
    """

    cdef int x, y

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "B(x=%s, y=%s)" % (self.x, self.y)

    def __reduce__(self):
        return makeB, ({'x': self.x, 'y': self.y},)

def makeB(kwds):
    return B(**kwds)
