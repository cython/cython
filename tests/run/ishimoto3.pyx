__doc__ = u"""
    >>> c1 = C1()
    >>> c2 = C2(c1)
    >>> c1 is c2.getc1()
    True
"""

cdef class C1:
    pass

cdef class C2:
    cdef C1 c1

    def __init__(self, arg):
        self.c1 = arg

    def getc1(self):
        return self.c1
