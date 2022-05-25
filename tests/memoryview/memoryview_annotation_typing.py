# mode: run
# tag: pep484, numpy, pure3.0
##, warnings

import cython
import numpy


def one_dim(a: cython.double[:]):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> one_dim(a)
    (2.0, 1)
    """
    a[0] *= 2
    return a[0], a.ndim


def one_dim_ccontig(a: cython.double[::1]):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> one_dim_ccontig(a)
    (2.0, 1)
    """
    a[0] *= 2
    return a[0], a.ndim


def two_dim(a: cython.double[:,:]):
    """
    >>> a = numpy.ones((10, 10), numpy.double)
    >>> two_dim(a)
    (3.0, 1.0, 2)
    """
    a[0,0] *= 3
    return a[0,0], a[0,1], a.ndim


@cython.nogil
@cython.cfunc
def _one_dim_nogil_cfunc(a: cython.double[:]) -> cython.double:
    a[0] *= 2
    return a[0]


def one_dim_nogil_cfunc(a: cython.double[:]):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> one_dim_nogil_cfunc(a)
    2.0
    """
    with cython.nogil:
        result = _one_dim_nogil_cfunc(a)
    return result
