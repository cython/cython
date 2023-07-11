import functools



@functools.total_ordering
cdef class ExtGe:
    cdef int x

    def __ge__(self, other):
        if not isinstance(other, ExtGe):
            return NotImplemented
        return self.x >= (<ExtGe>other).x

    def __eq__(self, other):
        return isinstance(other, ExtGe) and self.x == (<ExtGe>other).x
