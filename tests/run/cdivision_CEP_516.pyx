__doc__ = u"""
>>> v = [(17, 10), (-17, 10), (-17, -10), (17, -10)]
>>> standard = [(a % b) for a, b in v]
>>> standard
[7, 3, -7, -3]
>>> [mod_int_py(a, b) for a, b in v] == standard
True
>>> [mod_short_py(a, b) for a, b in v] == standard
True
>>> [mod_float_py(a, b) for a, b in v] == standard
True
>>> [mod_double_py(a, b) for a, b in v] == standard
True

>>> [mod_int_c(a, b) for a, b in v]
[7, -7, -7, 7]
>>> [mod_float_c(a, b) for a, b in v]
[7.0, -7.0, -7.0, 7.0]
>>> [mod_double_c(a, b) for a, b in v]
[7.0, -7.0, -7.0, 7.0]

>>> [div_int_py(a, b) for a, b in v]
[1, -2, 1, -2]
>>> [div_int_c(a, b) for a, b in v]
[1, -1, 1, -1]

>>> [test_cdiv_cmod(a, b) for a, b in v]
[(1, 7), (-1, -7), (1, -7), (-1, 7)]

>>> all([mod_int_py(a,b) == a % b for a in range(-10, 10) for b in range(-10, 10) if b != 0])
True
>>> all([div_int_py(a,b) == a // b for a in range(-10, 10) for b in range(-10, 10) if b != 0])
True

>>> def simple_warn(msg, *args): print msg
>>> import warnings
>>> warnings.showwarning = simple_warn

>>> mod_int_c_warn(-17, 10)
division with oppositely signed operands, C and Python semantics differ
-7
>>> div_int_c_warn(-17, 10)
division with oppositely signed operands, C and Python semantics differ
-1
>>> complex_expression(-150, 20, 20, -7)
verbose_call(-150)
division with oppositely signed operands, C and Python semantics differ
verbose_call(20)
division with oppositely signed operands, C and Python semantics differ
-2
"""

cimport cython

@cython.cdivision(False)
def mod_int_py(int a, int b):
    return a % b

@cython.cdivision(False)
def mod_short_py(short a, short b):
    return a % b

@cython.cdivision(False)
def mod_double_py(double a, double b):
    return a % b

@cython.cdivision(False)
def mod_float_py(float a, float b):
    return a % b

@cython.cdivision(True)
def mod_int_c(int a, int b):
    return a % b

@cython.cdivision(True)
def mod_float_c(float a, float b):
    return a % b

@cython.cdivision(True)
def mod_double_c(double a, double b):
    return a % b


@cython.cdivision(False)
def div_int_py(int a, int b):
    return a // b

@cython.cdivision(True)
def div_int_c(int a, int b):
    return a // b


@cython.cdivision(False)
def test_cdiv_cmod(short a, short b):
    cdef short q = cython.cdiv(a, b)
    cdef short r = cython.cmod(a, b)
    return q, r

@cython.cdivision(True)
@cython.cdivision_warnings(True)
def mod_int_c_warn(int a, int b):
    return a % b

@cython.cdivision(True)
@cython.cdivision_warnings(True)
def div_int_c_warn(int a, int b):
    return a // b

@cython.cdivision(False)
@cython.cdivision_warnings(True)
def complex_expression(int a, int b, int c, int d):
    return (verbose_call(a) // b) % (verbose_call(c) // d)

cdef int verbose_call(int x):
    print "verbose_call(%s)" % x
    return x
