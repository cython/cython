# tag: numpy
# tag: no-cpp
# Numpy <= 1.7.1 doesn't have a C++ guard in the header file.
# mode: run

cimport numpy.math as npmath
cimport libc.math as libc_math

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

    x = npmath.nextafterl(npmath.EULER, 1)
    assert npmath.isfinite(x)
    assert x >= npmath.EULER

    x = npmath.nextafterl(npmath.PI_4, -1)
    assert npmath.isfinite(x)
    assert x <= npmath.PI_4

    x = npmath.nextafterf(npmath.EULER, 1)
    assert npmath.isfinite(x)
    assert x > npmath.EULER

    x = npmath.nextafterf(npmath.PI_4, -1)
    assert npmath.isfinite(x)
    assert x < npmath.PI_4

def test_constants():
    """
    >>> test_constants()
    """
    assert libc_math.M_E == npmath.E
    assert libc_math.M_LOG2E == npmath.LOG2E
    assert libc_math.M_LOG10E == npmath.LOG10E
    assert libc_math.M_LN2 == npmath.LOGE2
    assert libc_math.M_LN10 == npmath.LOGE10
    assert libc_math.M_PI == npmath.PI
    assert libc_math.M_PI_2 == npmath.PI_2
    assert libc_math.M_PI_4 == npmath.PI_4
    assert libc_math.M_1_PI == npmath.NPY_1_PI
    assert libc_math.M_2_PI == npmath.NPY_2_PI
    # assert EULER == npmath.EULER  # libc_math has no EULER

def test_copysign():
    """
    >>> test_copysign()
    """
    assert libc_math.copysign(1., -1.) == npmath.copysign(1., -1.)
    assert libc_math.copysignf(1., -1.) == npmath.copysignf(1., -1.)
    assert libc_math.copysignl(1., -1.) == npmath.copysignl(1., -1.)


def test_spacing():
    """
    >>> test_spacing()
    """
    # Does not exist in libc.math
    assert npmath.spacing(1.) == npmath.nextafter(1., 3.) - 1.
    assert npmath.spacingf(1.) == npmath.nextafterf(1., 3.) - 1.
    assert npmath.spacingl(1.) == npmath.nextafterl(1., 3.) - 1.

def test_float99():
    """
    >>> test_float99()
    """
    # test existence, not accuracy
    assert libc_math.sinf(0) == npmath.sinf(0)
    assert libc_math.cosf(0) == npmath.cosf(0)
    assert libc_math.tanf(0) == npmath.tanf(0)
    assert libc_math.sinhf(0) == npmath.sinhf(0)
    assert libc_math.coshf(0) == npmath.coshf(0)
    assert libc_math.tanhf(0) == npmath.tanhf(0)
    assert libc_math.fabsf(0) == npmath.fabsf(0)
    assert libc_math.floorf(0) == npmath.floorf(0)
    assert libc_math.ceilf(0) == npmath.ceilf(0)
    assert libc_math.rintf(0) == npmath.rintf(0)
    assert libc_math.sqrtf(0) == npmath.sqrtf(0)
    assert libc_math.log10f(0) == npmath.log10f(0)
    assert libc_math.logf(0) == npmath.logf(0)
    assert libc_math.expf(0) == npmath.expf(0)
    assert libc_math.expm1f(0) == npmath.expm1f(0)
    assert libc_math.asinf(0) == npmath.asinf(0)
    assert libc_math.acosf(0) == npmath.acosf(0)
    assert libc_math.atanf(0) == npmath.atanf(0)
    assert libc_math.asinhf(1) == npmath.asinhf(1)
    assert libc_math.acoshf(1) == npmath.acoshf(1)
    assert libc_math.atanhf(1) == npmath.atanhf(1)
    assert libc_math.log1pf(0) == npmath.log1pf(0)
    assert libc_math.exp2f(0) == npmath.exp2f(0)
    assert libc_math.log2f(0) == npmath.log2f(0)
    assert libc_math.atan2f(0, 0) == npmath.atan2f(0, 0)
    assert libc_math.hypotf(0, 0) == npmath.hypotf(0, 0)
    assert libc_math.powf(0, 0) == npmath.powf(0, 0)
    assert libc_math.fmodf(1, 1) == npmath.fmodf(1, 1)

def test_longfloat99():
    """
    >>> test_longfloat99()
    """
    # test existence, not accuracy
    assert libc_math.sinl(0) == npmath.sinl(0)
    assert libc_math.cosl(0) == npmath.cosl(0)
    assert libc_math.tanl(0) == npmath.tanl(0)
    assert libc_math.sinhl(0) == npmath.sinhl(0)
    assert libc_math.coshl(0) == npmath.coshl(0)
    assert libc_math.tanhl(0) == npmath.tanhl(0)
    assert libc_math.fabsl(0) == npmath.fabsl(0)
    assert libc_math.floorl(0) == npmath.floorl(0)
    assert libc_math.ceill(0) == npmath.ceill(0)
    assert libc_math.rintl(0) == npmath.rintl(0)
    assert libc_math.sqrtl(0) == npmath.sqrtl(0)
    assert libc_math.log10l(0) == npmath.log10l(0)
    assert libc_math.logl(0) == npmath.logl(0)
    assert libc_math.expl(0) == npmath.expl(0)
    assert libc_math.expm1l(0) == npmath.expm1l(0)
    assert libc_math.asinl(1) == npmath.asinl(1)
    assert libc_math.acosl(1) == npmath.acosl(1)
    assert libc_math.atanl(1) == npmath.atanl(1)
    assert libc_math.asinhl(0) == npmath.asinhl(0)
    assert libc_math.acoshl(1) == npmath.acoshl(1)
    assert libc_math.atanhl(1) == npmath.atanhl(1)
    assert libc_math.log1pl(0) == npmath.log1pl(0)
    assert libc_math.exp2l(0) == npmath.exp2l(0)
    assert libc_math.log2l(0) == npmath.log2l(0)
    assert libc_math.atan2l(0,0 ) == npmath.atan2l(0, 0)
    assert libc_math.hypotl(0, 0) == npmath.hypotl(0, 0)
    assert libc_math.powl(0, 0) == npmath.powl(0, 0)
    assert libc_math.fmodf(1, 1) == npmath.fmodf(1, 1)

def test_extensions():
    """
    >>> test_extensions()
    """
    pass
    # TODO: test functions which does not exist in libc.math
    # modff, modfl
    # deg2radf, deg2rad, deg2radl
    # rad2degf, rad2deg, rad2degl
    # logaddexpf, logaddexp, logaddexpl
    # logaddexp2f, logaddex2p, logaddexp2l
