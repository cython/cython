__doc__ = """
    >>> len(Spam())
    0
"""

cdef class Spam:

    def __len__(self):
        return 0

