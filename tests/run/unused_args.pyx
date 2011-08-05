cdef c_unused_simple(a, b, c):
    """
    >>> c_unused_simple(1, 2, 3)
    3
    """
    return a + b

cdef c_unused_optional(a, b, c=1, d=2):
    """
    >>> c_unused_optional(1, 2)
    4
    >>> c_unused_optional(1, 2, 3, 4)
    6
    """
    return b + d

cpdef cp_unused_simple(a, b, c):
    """
    >>> cp_unused_simple(1, 2, 3)
    3
    """
    return a + b

cpdef cp_unused_optional(a, b, c=1, d=2):
    """
    >>> cp_unused_optional(1, 2)
    4
    >>> cp_unused_optional(1, 2, 3, 4)
    6
    """
    return b + d


cdef class Unused:
    """
    >>> o = Unused()
    """

    cpdef cp_unused_simple(self, a, b, c):
        return c

    cpdef cp_unused_optional(self, a, b, c=1, d=2):
        return b + d

def def_unused(a, b, c):
    """
    >>> def_unused(1, 2, 3)
    """

def def_unused_metho(o):
    """
    >>> def_unused_metho(0)
    """
