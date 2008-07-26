__doc__ = u"""
    >>> f = Fiche()
    >>> f[0] = 1
    >>> f.geti()
    1

    >>> f[1] = None
    >>> f.geti()
    0

    >>> f[0] = 1
    >>> f.geti()
    1
"""

cdef class Fiche:
    cdef int i

    def __setitem__(self, element, valeur):
        self.i = 0
        if valeur is None:
            return
        self.i = 1

    def geti(self):
        return self.i
