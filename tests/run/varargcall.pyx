cdef grail(char *blarg, ...):
    pass

def swallow():
    """
    >>> swallow()
    """
    grail("spam")
    grail("spam", 42)
