__doc__ = """
    >>> swallow()
"""

cdef grail(char *blarg, ...):
    pass

def swallow():
    grail("spam")
    grail("spam", 42)
