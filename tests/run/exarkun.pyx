__doc__ = u"""
    >>> p = Point(1,2,3)
    >>> p.gettuple()
    (1.0, 2.0, 3.0)
    >>> q = p + Point(2,3,4)
    >>> q.gettuple()
    (3.0, 5.0, 7.0)
    >>> p.gettuple()
    (1.0, 2.0, 3.0)
"""

cdef class Point:
    cdef double x, y, z
    def __init__(self, double x, double y, double z):
        self.x = x
        self.y = y
        self.z = z

    # XXX: originally, this said "def __add__(self, other)"
    def __add__(Point self, Point other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def gettuple(self):
        return (self.x, self.y, self.z)
