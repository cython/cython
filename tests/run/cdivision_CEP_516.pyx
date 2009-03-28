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

>>> mod_int_py_warn(-17, 10)
Warning: division with oppositely signed operands, C and Python semantics differ
-7
>>> div_int_py_warn(-17, 10)
Warning: division with oppositely signed operands, C and Python semantics differ
-1
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
def mod_int_py_warn(int a, int b):
    return a % b

@cython.cdivision(True)
@cython.cdivision_warnings(True)
def div_int_py_warn(int a, int b):
    return a // b
