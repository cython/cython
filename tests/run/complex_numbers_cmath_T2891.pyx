# ticket: 2891
# tag: c

cdef extern from "complex_numbers_c99_T398.h": pass

from libc.math cimport M_PI
from libc.complex cimport cimag, creal, cabs, carg


def test_decomposing(double complex z):
    """
    >>> test_decomposing(2j)
    (0.0, 2.0, 2.0, 0.5)

    >>> test_decomposing(2)
    (2.0, 0.0, 2.0, 0.0)

    >>> test_decomposing(-2j)
    (-0.0, -2.0, 2.0, -0.5)

    >>> test_decomposing(-2)
    (-2.0, 0.0, 2.0, 1.0)

    """
     
    return (creal(z), cimag(z), cabs(z), carg(z)/M_PI)
