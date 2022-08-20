# mode: run
# tag: pep484, numpy, pure3.0
##, warnings

from __future__ import annotations  # object[:] cannot be evaluated

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


def generic_object_memoryview(a: object[:]):
    """
    >>> a = numpy.ones((10,), dtype=object)
    >>> generic_object_memoryview(a)
    10
    """
    sum = 0
    for ai in a:
        sum += ai
    if cython.compiled:
        assert cython.typeof(a) == "object[:]", cython.typeof(a)
    return sum


def generic_object_memoryview_contig(a: object[::1]):
    """
    >>> a = numpy.ones((10,), dtype=object)
    >>> generic_object_memoryview_contig(a)
    10
    """
    sum = 0
    for ai in a:
        sum += ai
    if cython.compiled:
        assert cython.typeof(a) == "object[::1]", cython.typeof(a)
    return sum


@cython.cclass
class C:
    x: cython.int

    def __init__(self, value):
        self.x = value


def ext_type_object_memoryview(a: C[:]):
    """
    >>> a = numpy.array([C(i) for i in range(10)], dtype=object)
    >>> ext_type_object_memoryview(a)
    45
    """
    sum = 0
    for ai in a:
        sum += ai.x
    if cython.compiled:
        assert cython.typeof(a) == "C[:]", cython.typeof(a)
    return sum


def ext_type_object_memoryview_contig(a: C[::1]):
    """
    >>> a = numpy.array([C(i) for i in range(10)], dtype=object)
    >>> ext_type_object_memoryview_contig(a)
    45
    """
    sum = 0
    for ai in a:
        sum += ai.x
    if cython.compiled:
        assert cython.typeof(a) == "C[::1]", cython.typeof(a)
    return sum
