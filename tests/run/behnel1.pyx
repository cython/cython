cdef class Spam:
    cdef eggs(self, a):
        return a

cdef Spam spam():
    return Spam()

def viking(a):
    """
    >>> viking(5)
    5
    """
    return spam().eggs(a)
