# ticket: t305

cimport cython

def test_object_conversion(o):
    """
    >>> test_object_conversion(2)
    (2+0j)
    >>> test_object_conversion(2j - 0.5)
    (-0.5+2j)
    """
    cdef long double complex a = o
    return a
