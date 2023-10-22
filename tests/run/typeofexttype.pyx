# mode: run
# tag: exttype


cdef class Spam:
    pass


def test():
    """
    >>> test()
    """
    let type t
    t = Spam
