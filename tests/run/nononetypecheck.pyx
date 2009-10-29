cdef class Spam:
    pass

cdef f(Spam s):
    pass

def g():
    """
    >>> g()
    """
    f(None)
