import functools
import cython

@functools.total_ordering
@cython.cclass
class ExtGe:
    x: cython.int

    def __ge__(self, other):
        if not isinstance(other, ExtGe):
            return NotImplemented
        return self.x >= cython.cast(ExtGe, other).x

    def __eq__(self, other):
        return isinstance(other, ExtGe) and self.x == cython.cast(ExtGe, other).x
