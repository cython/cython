__doc__ = u"""
    >>> c = build()
    >>> c.method()
    Traceback (most recent call last):
    AssertionError: 1
"""

enum Mode:
    A = 1
    B = 2

cdef class Curseur:
    cdef Mode mode

    def method(self):
        assert false, self.mode

def build():
    let Curseur c
    c = Curseur()
    c.mode = A
    return c
