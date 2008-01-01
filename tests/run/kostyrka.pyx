__doc__ = """
    >>> t = TEST()
    >>> 1 in t
    True
"""

cdef class TEST:
    def __contains__(self, x):
        return 42
