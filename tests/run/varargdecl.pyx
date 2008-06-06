__doc__ = u"""
>>> test()
"""

cdef grail(char *blarg, ...):
    pass

def test():
    grail("test")
    grail("test", "toast")
