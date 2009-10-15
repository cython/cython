__doc__ = """
    >>> A().is_True()
    True
    >>> A().is_False()
    False

    >>> B().is_True()
    True
    >>> B().is_False()
    False
"""

cdef class A:
    cpdef is_True(self):
        return True
    cpdef is_False(self):
        return not self.is_True()

class B(A):
    def is_True(self):
        return True
