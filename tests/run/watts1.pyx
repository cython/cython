__doc__ = u"""
>>> test() == 55 + 66
True
"""


def test():
    cdef int a,b
    foo=(55,66)
    a,b=foo
    return a + b
