__doc__ = u"""
>>> test(3)
3
"""

def test(x):
    return retinput(x)

cdef inline int retinput(int x):
    o = x
    return o

