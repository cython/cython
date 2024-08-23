# mode: run
# tag: warnings

from __future__ import print_function

cimport cython


def pow_double_double(double a, double b, delta):
    """
    >>> pow_double_double(2, 2, 1e-15)
    soft double complex float
    >>> pow_double_double(4, 0.5, 1e-15)
    soft double complex float
    >>> pow_double_double(-4, 0.5, 1e-15)
    soft double complex complex
    """
    c = a**b
    # print out the Cython type, and the coerced type
    print(cython.typeof(c), type(c).__name__)
    object_c = (<object>a)**(<object>b)
    assert abs((c/object_c) - 1) < delta

@cython.cpow(True)
def pow_double_double_cpow(double a, double b, delta=None):
    """
    >>> pow_double_double_cpow(2, 2, 1e-15)
    double float
    >>> pow_double_double_cpow(4, 0.5, 1e-15)
    double float
    >>> x = pow_double_double_cpow(-4, 0.5)
    double float
    >>> x == x  # is nan
    False
    """
    c = a**b
    # print out the Cython type, and the coerced type
    print(cython.typeof(c), type(c).__name__)
    if delta is not None:
        object_c = (<object>a)**(<object>b)
        assert abs((c/object_c) - 1) < delta
    else:
        return c

cdef cfunc_taking_double(double x):
    return x

def pow_double_double_coerced_directly(double a, double b):
    """
    >>> pow_double_double_coerced_directly(2, 2)
    8.0
    >>> x = pow_double_double_coerced_directly(-2, 0.5)
    >>> x == x  # nan
    False
    """
    # Because we're assigning directly to a double assume 'cpow'
    # but warn.
    cdef double c = a**b
    return cfunc_taking_double(a**b) + c

def pow_double_int(double a, int b):
    """
    # a few variations of 'double**int'. In all cases
    # Cython should realise that the result can't be complex
    # and avoid going through the soft complex type
    >>> pow_double_int(5, 2)
    double
    double
    double
    double
    double
    """
    c1 = a**b
    c2 = a**2.0
    c3 = a**-2.0
    c4 = a**5
    c5 = a**-5
    print(cython.typeof(c1))
    print(cython.typeof(c2))
    print(cython.typeof(c3))
    print(cython.typeof(c4))
    print(cython.typeof(c5))

def soft_complex_coerced_to_double(double a, double b):
    """
    >>> soft_complex_coerced_to_double(2, 2)
    4.0
    >>> soft_complex_coerced_to_double(-2, 0.25)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert 'complex' with non-zero imaginary component to 'double' (this most likely comes from the '**' operator; use 'cython.cpow(True)' to return 'nan' instead of a complex number).
    """
    c = a**b
    assert cython.typeof(c) == "soft double complex"
    cdef double d = c  # will raise if complex
    return d

def soft_complex_coerced_to_complex(double a, double b):
    """
    >>> soft_complex_coerced_to_complex(2, 2)
    (4+0j)
    >>> x = soft_complex_coerced_to_complex(-1, 0.5)
    >>> abs(x.real) < 1e-15
    True
    >>> abs(x.imag - 1) < 1e-15
    True
    """
    # This is always fine, but just check it works
    c = a**b
    assert cython.typeof(c) == "soft double complex"
    cdef double complex d = c
    return d

def soft_complex_type_inference_1(double a, double b, pick):
    """
    >>> soft_complex_type_inference_1(2, 1, False)
    soft double complex 2.0
    >>> soft_complex_type_inference_1(2, 3, True)
    soft double complex 4.0
    """
    # double and soft complex should infer to soft-complex
    if pick:
        c = a**2
    else:
        c = a**b
    print(cython.typeof(c), c)

def soft_complex_type_inference_2(double a, double b, expected):
    """
    >>> soft_complex_type_inference_2(2, 1, 1.0)
    soft double complex
    >>> soft_complex_type_inference_2(2, 3, 7.0)
    soft double complex
    """
    # double and soft complex should infer to soft-complex
    c = a**b
    c -= 1
    print(cython.typeof(c))
    delta = abs(c/expected - 1)
    assert delta < 1e-15, delta

def pow_int_int(int a, int b):
    """
    >>> pow_int_int(2, 2)
    double 4.0
    >>> pow_int_int(2, -2)
    double 0.25
    """
    c = a**b
    print(cython.typeof(c), c)

@cython.cpow(True)
def pow_int_int_cpow(int a, int b):
    """
    >>> pow_int_int_cpow(2, 2)
    int 4
    >>> pow_int_int_cpow(2, -2)
    int 0
    """
    c = a**b
    print(cython.typeof(c), c)

cdef cfunc_taking_int(int x):
    return x

def pow_int_int_coerced_directly(int a, int b):
    """
    Generates two warnings about using cpow.
    The actual behaviour isn't too easy to distinguish
    without inspecting the c code though.
    >>> pow_int_int_coerced_directly(2, 2)
    8
    """
    cdef int c = a**b
    return cfunc_taking_int(a**b) + c

def pow_int_int_non_negative(int a, unsigned int b):
    """
    A couple of combinations of non-negative values for the
    exponent, which lets us fall back to int as a return type
    >>> pow_int_int_non_negative(5, 3)
    unsigned int
    long
    """
    c1 = a**b
    c2 = a**5
    print(cython.typeof(c1))
    print(cython.typeof(c2))


ctypedef double f64

def pythagoras_with_typedef(double a, double b):
    # see https://github.com/cython/cython/issues/5203
    """
    >>> rc = pythagoras_with_typedef(2.0, 2.0)
    >>> pyresult = 1.0 / (2 * 2.0 ** 2) ** 0.5
    >>> pyresult - 0.001 < rc < pyresult + 0.001  or  (rc, pyresult)
    True
    """
    cdef f64 result = a * a + b * b
    result = 1.0 / result ** 0.5
    return result


@cython.cpow(False)
def power_coercion_in_nogil_1(double a, double b):
    """
    >>> power_coercion_in_nogil_1(2., 2.)
    4.0
    >>> power_coercion_in_nogil_1(-1., 0.5)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert 'complex' with non-zero imaginary component to 'double' (this most likely comes from the '**' operator; use 'cython.cpow(True)' to return 'nan' instead of a complex number).
    """
    cdef double c
    with nogil:
        c = a**b
    return c


cdef double nogil_fun(double x) nogil:
    return x

def power_coercion_in_nogil_2(double a, double b):
    """
    >>> power_coercion_in_nogil_2(2., 2.)
    4.0
    >>> power_coercion_in_nogil_2(-1., 0.5)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert 'complex' with non-zero imaginary component to 'double' (this most likely comes from the '**' operator; use 'cython.cpow(True)' to return 'nan' instead of a complex number).
    """
    c = a**b
    with nogil:
        d = nogil_fun(c)
    return d


def power_coercion_in_nogil_3(double a, double b, double c):
    """
    >>> power_coercion_in_nogil_3(2., 2., 1.0)
    0.25
    >>> power_coercion_in_nogil_3(-1., 0.5, 1.0)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert 'complex' with non-zero imaginary component to 'double' (this most likely comes from the '**' operator; use 'cython.cpow(True)' to return 'nan' instead of a complex number).
    """
    with nogil:
        c /= a**b
    return c


_WARNINGS = """
58:21: Treating '**' as if 'cython.cpow(True)' since it is directly assigned to a a non-complex C numeric type. This is likely to be fragile and we recommend setting 'cython.cpow' explicitly.
59:32: Treating '**' as if 'cython.cpow(True)' since it is directly assigned to a a non-complex C numeric type. This is likely to be fragile and we recommend setting 'cython.cpow' explicitly.
174:18: Treating '**' as if 'cython.cpow(True)' since it is directly assigned to a an integer C numeric type. This is likely to be fragile and we recommend setting 'cython.cpow' explicitly.
175:29: Treating '**' as if 'cython.cpow(True)' since it is directly assigned to a an integer C numeric type. This is likely to be fragile and we recommend setting 'cython.cpow' explicitly.
"""
