# mode: run
# tag: pickle, memoryview
# ticket: 6767

cdef class NoReduceDueToMemoryview:
    """
    >>> import pickle
    >>> pickle.dumps(NoReduceDueToMemoryview())
    Traceback (most recent call last):
    ...
    TypeError: self.x cannot be pickled because typed memoryviews are not pickleable
    """
    cdef double[:, :] x


cdef class NoReduceDueToInheritedMemoryview(NoReduceDueToMemoryview):
    """
    >>> import pickle
    >>> pickle.dumps(NoReduceDueToInheritedMemoryview())
    Traceback (most recent call last):
    ...
    TypeError: self.x cannot be pickled because typed memoryviews are not pickleable
    """
