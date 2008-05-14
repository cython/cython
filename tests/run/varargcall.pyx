__doc__ = u"""
    >>> swallow()
"""

cdef grail(char *blarg, ...):
    pass

def swallow():
    grail("spam")
    grail("spam", 42)
