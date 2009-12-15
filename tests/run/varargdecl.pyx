cdef grail(char *blarg, ...):
    pass

def test():
    """
    >>> test()
    """
    grail(b"test")
    grail(b"test", b"toast")
