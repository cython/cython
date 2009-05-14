__doc__ = u"""
    >>> test_object_conversion(2)
    ((2+0j), (2+0j))
    >>> test_object_conversion(2j - 0.5)
    ((-0.5+2j), (-0.5+2j))
    
    >>> test_arithmetic(2j, 4j)
    (-2j, 6j, -2j, (-8+0j), (0.5+0j))
    >>> test_arithmetic(6+12j, 3j)
    ((-6-12j), (6+15j), (6+9j), (-36+18j), (4-2j))
    >>> test_arithmetic(5-10j, 3+4j)
    ((-5+10j), (8-6j), (2-14j), (55-10j), (-1-2j))

    >>> test_div_by_zero(4j)
    -0.25j
    >>> test_div_by_zero(0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: float division

    >>> test_coercion(1, 1.5, 2.5, 4+1j, 10j)
    (1+0j)
    (1.5+0j)
    (2.5+0j)
    (4+1j)
    10j
    (9+21j)
    
    >>> test_compare(3, 3)
    (True, False)
    >>> test_compare(3j, 3j)
    (True, False)
    >>> test_compare(3j, 4j)
    (False, True)
    >>> test_compare(3, 4)
    (False, True)
    
    >>> test_compare_coerce(3, 4)
    (False, True)
    >>> test_compare_coerce(4+1j, 4)
    (False, True)
    >>> test_compare_coerce(4, 4)
    (True, False)
    
    >>> test_literal()
    (5j, (1-2.5j))
    
    >>> test_real_imag(1-3j)
    (1.0, -3.0)
    >>> test_real_imag(5)
    (5.0, 0.0)
    >>> test_real_imag(1.5j)
    (0.0, 1.5)
    
    >>> test_real_imag_assignment(1, 2)
    (1+2j)
    >>> test_real_imag_assignment(1.5, -3.5)
    (1.5-3.5j)
"""

#cdef extern from "complex.h":
#    pass

cimport cython

def test_object_conversion(o):
    cdef float complex a = o
    cdef double complex z = o
    return (a, z)

def test_arithmetic(double complex z, double complex w):
    return -z, z+w, z-w, z*w, z/w

@cython.cdivision(False)
def test_div_by_zero(double complex z):
    return 1/z

def test_coercion(int a, float b, double c, float complex d, double complex e):
    cdef double complex z
    z = a; print z
    z = b; print z
    z = c; print z
    z = d; print z
    z = e; print z
    return z + a + b + c + d + e

def test_compare(double complex a, double complex b):
    return a == b, a != b

def test_compare_coerce(double complex a, int b):
    return a == b, a != b

def test_literal():
    return 5j, 1-2.5j

def test_real_imag(double complex z):
    return z.real, z.imag

def test_real_imag_assignment(object a, double b):
    cdef double complex z
    z.real = a
    z.imag = b
    return z

