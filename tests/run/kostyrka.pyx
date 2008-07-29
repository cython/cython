__doc__ = u"""
    >>> t = TEST()
    >>> 1 in t
    True
"""

cdef class TEST:
    def __contains__(self, x):
        return 42
