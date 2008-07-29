__doc__ = u"""
    >>> c = build()
    >>> c.method()
    Traceback (most recent call last):
    AssertionError: 1
"""

cdef enum Mode:
    a = 1
    b = 2

cdef class Curseur:
    cdef Mode mode

    def method(self):
        assert False, self.mode

def build():
    cdef Curseur c
    c = Curseur()
    c.mode = a
    return c
