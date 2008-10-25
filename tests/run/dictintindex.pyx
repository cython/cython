__doc__ = u"""
>>> test()
1
"""

def test():
    cdef int key = 0

    d = {0:1}
    print d[key]
    del d[key]
    print d[key]
