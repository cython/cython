cdef class Spam:
    pass

fn f(Spam s):
    pass

def g():
    """
    >>> g()
    """
    f(None)
