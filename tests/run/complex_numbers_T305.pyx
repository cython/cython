# ticket: 305

cimport cython

def test_object_conversion(o):
    """
    >>> test_object_conversion(2)
    ((2+0j), (2+0j), (2+0j))
    >>> test_object_conversion(2j - 0.5)
    ((-0.5+2j), (-0.5+2j), (-0.5+2j))
    """
    cdef float complex a = o
    cdef double complex b = o
    cdef long double complex c = o
    return (a, b, c)

def test_arithmetic(double complex z, double complex w):
    """
    >>> test_arithmetic(2j, 4j)
    (2j, -2j, 6j, -2j, (-8+0j), (0.5+0j))
    >>> test_arithmetic(6+12j, 3j)
    ((6+12j), (-6-12j), (6+15j), (6+9j), (-36+18j), (4-2j))
    >>> test_arithmetic(5-10j, 3+4j)
    ((5-10j), (-5+10j), (8-6j), (2-14j), (55-10j), (-1-2j))
    """
    return +z, -z+0, z+w, z-w, z*w, z/w

def test_pow(double complex z, double complex w, tol=None):
    """
    Various implementations produce slightly different results...

    >>> a = complex(3, 1)
    >>> test_pow(a, 1, 1e-15)
    True
    >>> test_pow(a, 2, 1e-15)
    True
    >>> test_pow(a, a, 1e-15)
    True
    >>> test_pow(complex(0.5, -.25), complex(3, 4), 1e-15)
    True
    """
    if tol is None:
        return z**w
    else:
        return abs(z**w / <object>z ** <object>w - 1) < tol

def test_int_pow(double complex z, int n, tol=None):
    """
    >>> [test_int_pow(complex(0, 1), k, 1e-15) for k in range(-4, 5)]
    [True, True, True, True, True, True, True, True, True]
    >>> [test_int_pow(complex(0, 2), k, 1e-15) for k in range(-4, 5)]
    [True, True, True, True, True, True, True, True, True]
    >>> [test_int_pow(complex(2, 0.5), k, 1e-14) for k in range(0, 10)]
    [True, True, True, True, True, True, True, True, True, True]
    """
    if tol is None:
        return z**n + <object>0 # add zero to normalize zero sign
    else:
        return abs(z**n / <object>z ** <object>n - 1) < tol

@cython.cdivision(False)
def test_div_by_zero(double complex z):
    """
    >>> test_div_by_zero(4j)
    -0.25j
    >>> test_div_by_zero(0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: float division
    """
    return 1/z

def test_coercion(int a, float b, double c, float complex d, double complex e):
    """
    >>> test_coercion(1, 1.5, 2.5, 4+1j, 10j)
    (1+0j)
    (1.5+0j)
    (2.5+0j)
    (4+1j)
    10j
    (9+21j)
    """
    cdef double complex z
    z = a; print z
    z = b; print z
    z = c; print z
    z = d; print z
    z = e; print z
    return z + a + b + c + d + e

def test_compare(double complex a, double complex b):
    """
    >>> test_compare(3, 3)
    (True, False)
    >>> test_compare(3j, 3j)
    (True, False)
    >>> test_compare(3j, 4j)
    (False, True)
    >>> test_compare(3, 4)
    (False, True)
    """
    return a == b, a != b

def test_compare_coerce(double complex a, int b):
    """
    >>> test_compare_coerce(3, 4)
    (False, True)
    >>> test_compare_coerce(4+1j, 4)
    (False, True)
    >>> test_compare_coerce(4, 4)
    (True, False)
    """
    return a == b, a != b

def test_literal():
    """
    >>> test_literal()
    (5j, (1-2.5j))
    """
    return 5j, 1-2.5j

def test_real_imag(double complex z):
    """
    >>> test_real_imag(1-3j)
    (1.0, -3.0)
    >>> test_real_imag(5)
    (5.0, 0.0)
    >>> test_real_imag(1.5j)
    (0.0, 1.5)
    """
    return z.real, z.imag

def test_real_imag_assignment(object a, double b):
    """
    >>> test_real_imag_assignment(1, 2)
    (1+2j)
    >>> test_real_imag_assignment(1.5, -3.5)
    (1.5-3.5j)
    """
    cdef double complex z
    z.real = a
    z.imag = b
    return z

def test_conjugate(float complex z):
    """
    >>> test_conjugate(2+3j)
    (2-3j)
    """
    return z.conjugate()

def test_conjugate_double(double complex z):
    """
    >>> test_conjugate_double(2+3j)
    (2-3j)
    """
    return z.conjugate()

ctypedef double complex cdouble
def test_conjugate_typedef(cdouble z):
    """
    >>> test_conjugate_typedef(2+3j)
    (2-3j)
    """
    return z.conjugate()

cdef cdouble test_conjugate_nogil(cdouble z) nogil:
    # Really just a compile test.
    return z.conjugate()
test_conjugate_nogil(0) # use it

## cdef extern from "complex_numbers_T305.h":
##     ctypedef double double_really_float "myfloat"
##     ctypedef float float_really_double "mydouble"
##     ctypedef float real_float "myfloat"
##     ctypedef double real_double "mydouble"

## def test_conjugate_nosizeassumptions(double_really_float x,
##                                      float_really_double y,
##                                      real_float z, real_double w):
##     """
##     >>> test_conjugate_nosizeassumptions(1, 1, 1, 1)
##     (-1j, -1j, -1j, -1j)
##     >>> ["%.2f" % x.imag for x in test_conjugate_nosizeassumptions(2e300, 2e300, 2e300, 2e300)]
##     ['-inf', '-2e+300', '-inf', '-2e+300']
##     """
##     cdef double complex I = 1j
##     return ((x*I).conjugate(), (y*I).conjugate(), (z*I).conjugate(), (w*I).conjugate())

ctypedef double mydouble
def test_coerce_typedef_multiply(mydouble x, double complex z):
    """
    >>> test_coerce_typedef_multiply(3, 1+1j)
    (3+3j)
    """
    return x * z

ctypedef int myint
def test_coerce_typedef_multiply_int(myint x, double complex z):
    """
    >>> test_coerce_typedef_multiply_int(3, 1+1j)
    (3+3j)
    """
    return x * z

cpdef double complex complex_retval():
    """
    >>> complex_retval()
    1j
    """
    return 1j
