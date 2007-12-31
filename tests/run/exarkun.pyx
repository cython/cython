cdef class Point:
    cdef double x, y, z
    def __init__(self, double x, double y, double z):
        self.x = x
        self.y = y
        self.z = z

    # XXX
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
