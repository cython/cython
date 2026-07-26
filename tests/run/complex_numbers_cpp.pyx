# tag: cpp

import math
cimport libcpp.complex as cppcomplex
from libcpp.complex cimport complex as complex_class

def double_complex(complex_class[double] a):
    """
    >>> double_complex(1 + 2j)
    (1+2j)
    >>> double_complex(1.5 + 2.5j)
    (1.5+2.5j)
    """
    return a

def double_int(complex_class[int] a):
    """
    >>> double_int(1 + 2j)
    (1+2j)
    >>> double_int(1.5 + 2.5j)
    (1+2j)
    """
    return a

def double_addition_with_scalar(complex_class[double] a, double b):
    """
    >>> double_addition_with_scalar(1 + 1j, 1) + 1
    (3+1j)
    >>> 1 + double_addition_with_scalar(1 + 2j, -1)
    (1+2j)
    >>> 1j + double_addition_with_scalar(1 + 2j, 7)
    (8+3j)
    >>> double_addition_with_scalar(1 + 2j, 7) - 1j
    (8+1j)
    >>> double_addition_with_scalar(1.5 + 2.5j, -1) + 0
    (0.5+2.5j)
    >>> -0 + double_addition_with_scalar(1.5 + 2.5j, -1)
    (0.5+2.5j)
    """
    cdef complex_class[double] c = a + b
    cdef complex_class[double] d = b + a
    return b + a

def double_inplace_addition_with_scalar(complex_class[double] a, double b):
    """
    >>> double_inplace_addition_with_scalar(1 + 1j, 1)
    (2+1j)
    """
    a += b
    return a

def double_inplace_substraction_with_scalar(complex_class[double] a, double b):
    """
    >>> double_inplace_substraction_with_scalar(1 + 1j, 2)
    (-1+1j)
    """
    a -= b
    return a

def double_inplace_multiplication_with_scalar(complex_class[double] a, double b):
    """
    >>> double_inplace_multiplication_with_scalar(1 + 1j, 2)
    (2+2j)
    """
    a *= b
    return a

def double_inplace_division_with_scalar(complex_class[double] a, double b):
    """
    >>> double_inplace_division_with_scalar(3 + 3j, 2)
    (1.5+1.5j)
    """
    a /= b
    return a

def double_unary_negation(complex_class[double] a):
    """
    >>> double_unary_negation(2 + 2j)
    (-2-2j)
    """
    return -a

def double_unary_positive(complex_class[double] a):
    """
    >>> double_unary_positive(2 + 2j)
    (2+2j)
    """
    return +a

def double_real_imaginary_accessors(complex_class[double] a, double real, double imag):
    """
    >>> a = double_real_imaginary_accessors(2.1 + 2j, 7, 4)
    >>> a.real
    9.1
    >>> a.imag
    6.0
    """
    # checks the accessors
    cdef double b = a.real()
    a.real(b + real)

    cdef double c = a.imag()
    a.imag(c + imag)

    return a

def double_double_comparison_equal(complex_class[double] a, complex_class[double] b):
    """
    >>> double_double_comparison_equal(2.1 + 2j, 7)
    False
    >>> double_double_comparison_equal(2.1 + 2j, (1j + 1) * 2 + 0.1)
    True
    """
    return a == b

def double_scalar_double_comparison_equal(complex_class[double] a, double b):
    """
    >>> double_double_comparison_equal(2.1 + 2j, 7)
    False
    >>> double_double_comparison_equal(7 + 0j, 7)
    True
    """
    return a == b

def scalar_double_double_comparison_equal(complex_class[double] a, double b):
    """
    >>> double_double_comparison_equal(2.1 + 2j, 7)
    False
    >>> double_double_comparison_equal(7 + 0j, 7)
    True
    """
    return b == a

def double_real_imaginary_accessors_free_function(complex_class[double] a, bint real_part):
    """
    >>> double_real_imaginary_accessors_free_function(2.1 + 2.7j, True)
    2.1
    >>> double_real_imaginary_accessors_free_function(2.1 + 2.7j, False)
    2.7
    """

    cdef double e = cppcomplex.real(a)
    cdef double f = cppcomplex.imag(a)
    if real_part:
        return e
    return f

def scalar_double_real_imaginary_accessors_free_function(double a, bint real_part):
    """
    >>> scalar_double_real_imaginary_accessors_free_function(2.1, True)
    2.1
    >>> scalar_double_real_imaginary_accessors_free_function(2.1, False)
    0.0
    """
    cdef double e = cppcomplex.real(a)
    cdef double f = cppcomplex.imag(a)
    if real_part:
        return e
    return f

def scalar_long_double_real_imaginary_accessors_free_function(long double a, bint real_part):
    """
    >>> scalar_long_double_real_imaginary_accessors_free_function(2.1, True)
    2.1
    >>> scalar_long_double_real_imaginary_accessors_free_function(2.1, False)
    0.0
    """
    cdef double e = cppcomplex.real(a)
    cdef double f = cppcomplex.imag(a)
    if real_part:
        return e
    return f

def double_abs(complex_class[double] a):
    """
    >>> double_abs(5)
    5.0
    >>> double_abs(5j)
    5.0
    >>> double_abs(2 + 5j) == math.sqrt(29)
    True
    """
    return cppcomplex.abs(a)

def double_norm(complex_class[double] a):
    """
    >>> double_norm(5)
    25.0
    >>> double_norm(5j)
    25.0
    >>> abs(double_norm(2 + 5j) - double_abs(2 + 5j)*double_abs(2 + 5j)) < 1e-13
    True
    """
    return cppcomplex.norm(a)

def scalar_double_norm(double a):
    """
    >>> scalar_double_norm(5)
    25.0
    """
    return cppcomplex.norm(a)

def scalar_float_norm(float a):
    """
    >>> scalar_float_norm(5)
    25.0
    """
    return cppcomplex.norm(a)

def double_conjugate(complex_class[double] a):
    """
    >>> double_conjugate(5)
    (5-0j)
    >>> double_conjugate(5j)
    -5j
    >>> double_conjugate(1 + 2j)
    (1-2j)
    """
    return cppcomplex.conj(a)

def scalar_double_conjugate(double a):
    """
    >>> a = scalar_double_conjugate(5)
    >>> a.real
    5.0
    >>> # abs to prevent -0 or 0 issue
    >>> abs(a.imag)
    0.0
    """
    # always return complex
    return cppcomplex.conj(a)

def double_proj(complex_class[double] a):
    """
    >>> double_proj(5 + 4j)
    (5+4j)
    >>> double_proj(-float("infinity") + 4j)
    (inf+0j)
    >>> double_proj(5 - float("infinity")*1j)
    (inf-0j)
    """
    return cppcomplex.proj(a)

def double_arg(complex_class[double] a):
    """
    >>> a = math.pi / 4
    >>> round(a, 10)
    0.7853981634
    >>> round(double_arg(math.cos(a) + math.sin(a)*1j), 10)
    0.7853981634
    """
    return cppcomplex.arg(a)

def scalar_double_arg(double a):
    """
    >>> scalar_double_arg(13)
    0.0
    >>> round(scalar_double_arg(-1), 10)
    3.1415926536
    """
    return cppcomplex.arg(a)

def double_polar(double r, double theta):
    """
    >>> c1 = double_polar(3, math.pi / 2)
    >>> c1.imag
    3.0
    >>> abs(c1.real) < 1e-10
    True
    >>> c2 = double_polar(4, math.pi)
    >>> c2.real
    -4.0
    >>> abs(c2.imag) < 1e-10
    True
    """
    return cppcomplex.polar(r, theta)

def double_polar_scalar(double r):
    """
    >>> c1 = double_polar_scalar(3)
    >>> c1.real
    3.0
    >>> c1.imag
    0.0
    >>> c2 = double_polar_scalar(0)
    >>> c2.real
    0.0
    >>> c2.imag
    0.0
    """
    return cppcomplex.polar(r)

def double_pow(complex_class[double] a, complex_class[double] b):
    """
    >>> double_pow(3, 3)
    (27+0j)
    >>> a = double_pow(1j, 1j)
    >>> round(a.real, 5)
    0.20788
    >>> round(a.imag, 2)
    0.0
    """
    return cppcomplex.pow(a, b)

def double_scalar_double_pow(complex_class[double] a, double b):
    """
    >>> double_pow(3, 3)
    (27+0j)
    >>> a = double_pow(1+2j, 2)
    >>> round(a.real, 2)
    -3.0
    >>> round(a.imag, 2)
    4.0
    """
    return cppcomplex.pow(a, b)

def scalar_double_double_pow(double a, complex_class[double] b):
    """
    >>> scalar_double_double_pow(3, 3)
    (27+0j)
    >>> a = scalar_double_double_pow(2, 2j)
    >>> round(a.real, 2)
    0.18
    >>> round(a.imag, 2)
    0.98
    """
    return cppcomplex.pow(a, b)

def double_sin(complex_class[double] a):
    """
    >>> round(abs(double_sin(math.pi)), 2)
    0.0
    >>> round(double_sin(-math.pi/4).real, 3)
    -0.707
    >>> round(abs(double_sin(-math.pi/4).imag), 3)
    0.0
    >>> round(abs(double_sin(4j).real), 3)
    0.0
    >>> round(abs(double_sin(4j).imag - math.sinh(4)), 3)
    0.0
    """
    return cppcomplex.sin(a)

def double_cos(complex_class[double] a):
    """
    >>> round(double_cos(math.pi).real, 2)
    -1.0
    >>> round(abs(double_cos(math.pi).imag), 2)
    0.0
    >>> round(double_cos(-math.pi/4 + math.pi).real, 3)
    -0.707
    >>> round(abs(double_cos(-math.pi/4).imag), 3)
    0.0
    >>> round(abs(double_cos(4j).imag), 3)
    0.0
    >>> round(abs(double_cos(5j).real - math.cosh(5)), 3)
    0.0
    """
    return cppcomplex.cos(a)
