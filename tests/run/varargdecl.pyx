__doc__ = u"""
>>> test()
"""

cdef grail(char *blarg, ...):
    pass

def test():
    grail(b"test")
    grail(b"test", b"toast")
