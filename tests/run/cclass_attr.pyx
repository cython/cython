# mode: run

cdef class CReserved:
    """
    >>> cr = CReserved()
    >>> cr.default
    1
    >>> cr.void
    2
    """
    cdef readonly int default
    cdef public int void

    def __init__(self):
        self.default = 1
        self.void = 2
