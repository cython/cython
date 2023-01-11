# mode: run

from cpython.number cimport PyNumber_InPlacePower

def ipow(a, b, c):
    # As far as DW can tell, calling through this C API call is the
    # only way to actually use ternary __ipow__
    return PyNumber_InPlacePower(a, b, c)

# three-arg ipow can only work safely on Py3.8+
# and so tests are in a separate file

cdef class TwoOrThreeArgIPow:
    """
    >>> a = TwoOrThreeArgIPow('a')
    >>> a**=2
    >>> print(a)
    a**2[None]
    >>> print(ipow(TwoOrThreeArgIPow('a'), 'x', 'y'))
    a**x[y]
    """
    cdef str name

    def __init__(self, name):
        self.name = name

    def __ipow__(self, other, base=None):
        return f"{self.name}**{other}[{base}]"


cdef class ThreeArgIPow:
    """
    Note that it's not possible to detect if this is called in a 2-arg context
    since the Python interpreter just passes None
    >>> a = ThreeArgIPow('a')
    >>> a**=2
    >>> print(a)
    a**2[None]
    >>> print(ipow(ThreeArgIPow('a'), 'x', 'y'))
    a**x[y]
    """
    cdef str name

    def __init__(self, name):
        self.name = name

    def __ipow__(self, other, base):
        return f"{self.name}**{other}[{base}]"
