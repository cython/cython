__doc__ = u"""

    >>> hash(A(5))
    5
    >>> hash(A(-1))
    -2
    >>> hash(A(-2))
    -2
    >>> hash(A(100))
    Traceback (most recent call last):
    ...
    TypeError: That's kind of a round number...
    
    >>> __hash__(-1)
    -1
"""

cdef class A:
    cdef long a
    def __init__(self, a):
        self.a = a
    def __hash__(self):
        if self.a == 100:
            raise TypeError, "That's kind of a round number..."
        else:
            return self.a

cpdef long __hash__(long x):
    return x
