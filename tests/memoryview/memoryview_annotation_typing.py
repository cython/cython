# mode: run
# tag: pep484, numpy, pure3.7
##, warnings

from __future__ import annotations  # object[:] cannot be evaluated

import cython
try:
    import typing
except ImportError:
    pass  # Workaround for python 2.7
import numpy

COMPILED = cython.compiled

def one_dim(a: cython.double[:]):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> one_dim(a)
    (2.0, 1)
    """
    a[0] *= 2
    return float(a[0]), a.ndim


def one_dim_ccontig(a: cython.double[::1]):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> one_dim_ccontig(a)
    (2.0, 1)
    """
    a[0] *= 2
    return float(a[0]), a.ndim


def two_dim(a: cython.double[:,:]):
    """
    >>> a = numpy.ones((10, 10), numpy.double)
    >>> two_dim(a)
    (3.0, 1.0, 2)
    """
    a[0,0] *= 3
    return float(a[0,0]), float(a[0,1]), a.ndim


def variable_annotation(a):
    """
    >>> a = numpy.ones((10,), numpy.double)
    >>> variable_annotation(a)
    2.0
    """
    b: cython.double[:]
    b = None

    if cython.compiled:
        assert cython.typeof(b) == "double[:]",  cython.typeof(b)

    b = a
    b[1] += 1
    b[2] += 2
    return float(b[1])


def slice_none(m: cython.double[:]):
    """
    >>> try:
    ...     a = slice_none(None)
    ... except TypeError as exc:
    ...     assert COMPILED
    ...     if "Argument 'm' must not be None" not in str(exc): raise
    ... else:
    ...     assert a == 1
    ...     assert not COMPILED
    """
    return 1 if m is None else 2


def slice_optional(m: typing.Optional[cython.double[:]]):
    """
    >>> slice_optional(None)
    1
    >>> a = numpy.ones((10,), numpy.double)
    >>> slice_optional(a)
    2

    # Make sure that we actually evaluate the type and don't just accept everything.
    >>> try:
    ...     x = slice_optional(123)
    ... except TypeError as exc:
    ...     if not COMPILED: raise
    ... else:
    ...     assert not COMPILED
    """
    return 1 if m is None else 2

def slice_union(m: typing.Union[cython.double[:], None]):
    """
    >>> slice_union(None)
    1
    >>> a = numpy.ones((10,), numpy.double)
    >>> slice_union(a)
    2

    # Make sure that we actually evaluate the type and don't just accept everything.
    >>> try:
    ...     x = slice_union(123)
    ... except TypeError as exc:
    ...     if not COMPILED: raise
    ... else:
    ...     assert not COMPILED
    """
    return 1 if m is None else 2

def slice_bitwise_or_none(m: cython.double[:] | None, n: None | cython.double[:]):
    """
    >>> slice_bitwise_or_none(None, None)
    (1, 1)
    >>> a = numpy.ones((10,), numpy.double)
    >>> slice_bitwise_or_none(a, a)
    (2, 2)

    # Make sure that we actually evaluate the type and don't just accept everything.
    >>> try:
    ...     x = slice_bitwise_or_none(123, None)
    ... except TypeError as exc:
    ...     if not COMPILED: raise
    ... else:
    ...     assert not COMPILED

    >>> try:
    ...     x = slice_bitwise_or_none(None, 123)
    ... except TypeError as exc:
    ...     if not COMPILED: raise
    ... else:
    ...     assert not COMPILED
    """
    return (1 if m is None else 2, 1 if n is None else 2)

@cython.nogil
@cython.cfunc
def _one_dim_nogil_cfunc(a: cython.double[:]) -> cython.double:
    a[0] *= 2
    return float(a[0])


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
