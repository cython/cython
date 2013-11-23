# mode: run
# tag: exttype


cdef class Spam:
    pass


def test():
    """
    >>> test()
    """
    cdef type t
    t = Spam
