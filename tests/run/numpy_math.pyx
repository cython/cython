# tag: numpy
# tag: no-cpp
# Numpy <= 1.7.1 doesn't have a C++ guard in the header file.

cimport numpy.math as npmath


def test_fp_classif():
    """
    >>> test_fp_classif()
    """

    cdef double d_zero
    cdef float f_zero

    d_zero = -1 * 0.
    f_zero = -1 * 0.

    assert d_zero == npmath.NZERO
    assert f_zero == npmath.NZERO

    assert npmath.signbit(d_zero)
    assert npmath.signbit(f_zero)

    d_zero = 1 * 0.
    f_zero = 1 * 0.

    assert d_zero == npmath.PZERO
    assert f_zero == npmath.PZERO

    assert not npmath.signbit(d_zero)
    assert not npmath.signbit(f_zero)

    assert not npmath.isinf(d_zero)
    assert not npmath.isinf(f_zero)

    assert not npmath.isnan(d_zero)
    assert not npmath.isnan(f_zero)

    assert npmath.isinf(-npmath.INFINITY)
    assert npmath.isinf(npmath.INFINITY)
    assert npmath.isnan(npmath.NAN)

    assert npmath.signbit(npmath.copysign(1., -1.))


def test_nextafter():
    """
    >>> test_nextafter()
    """

    x = npmath.nextafter(npmath.EULER, 1)
    assert npmath.isfinite(x)
    assert x > npmath.EULER

    x = npmath.nextafter(npmath.PI_4, -1)
    assert npmath.isfinite(x)
    assert x < npmath.PI_4
