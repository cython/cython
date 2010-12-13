cdef class A:
    def numerator(self):
        return self

cdef int  bitsize(A a):
    return 1

coeffs = [A()]

class B:
    """
    >>> B().coeffs_bitsize()
    [2]
    """
    def coeffs_bitsize(self):
        r = [bitsize(c.numerator())+1 for c in coeffs]
        return r
