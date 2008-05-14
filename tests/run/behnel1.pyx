__doc__ = u"""
    >>> viking(5)
    5
"""

cdef class Spam:
    cdef eggs(self, a):
        return a

cdef Spam spam():
    return Spam()

def viking(a):
    return spam().eggs(a)
