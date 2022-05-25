from __future__ import division

cimport cython


def bigints(values):
    for x in values:
        print(repr(x).rstrip('L'))


def doit(x,y):
    """
    >>> doit(1,2)
    (0.5, 0)
    >>> doit(4,3)
    (1.3333333333333333, 1)
    >>> doit(4,3.0)
    (1.3333333333333333, 1.0)
    >>> doit(4,2)
    (2.0, 2)
    """
    return x/y, x//y

def doit_inplace(x,y):
    """
    >>> doit_inplace(1,2)
    0.5
    """
    x /= y
    return x

def doit_inplace_floor(x,y):
    """
    >>> doit_inplace_floor(1,2)
    0
    """
    x //= y
    return x

def constants():
    """
    >>> constants()
    (0.5, 0, 2.5, 2.0, 2.5, 2)
    """
    return 1/2, 1//2, 5/2.0, 5//2.0, 5/2, 5//2


def py_mix(a):
    """
    >>> py_mix(1)
    (0.5, 0, 0.5, 0.0, 0.5, 0)
    >>> py_mix(1.0)
    (0.5, 0.0, 0.5, 0.0, 0.5, 0.0)
    >>> 2**53 / 2.0
    4503599627370496.0
    >>> bigints(py_mix(2**53))
    4503599627370496.0
    4503599627370496
    4503599627370496.0
    4503599627370496.0
    4503599627370496.0
    4503599627370496
    >>> bigints(py_mix(2**53 + 1))
    4503599627370496.0
    4503599627370496
    4503599627370496.0
    4503599627370496.0
    4503599627370496.0
    4503599627370496
    >>> py_mix(2**53 + 1.0)
    (4503599627370496.0, 4503599627370496.0, 4503599627370496.0, 4503599627370496.0, 4503599627370496.0, 4503599627370496.0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2


def py_mix_by_neg1(a):
    """
    >>> py_mix_by_neg1(0)
    (-0.0, 0, -0.0, -0.0, -0.0, 0)
    >>> py_mix_by_neg1(-1)
    (1.0, 1, 1.0, 1.0, 1.0, 1)
    >>> py_mix_by_neg1(int(2**31-1))
    (-2147483647.0, -2147483647, -2147483647.0, -2147483647.0, -2147483647.0, -2147483647)
    >>> bigints(py_mix_by_neg1(int(-2**31-1)))
    2147483649.0
    2147483649
    2147483649.0
    2147483649.0
    2147483649.0
    2147483649
    >>> results = py_mix_by_neg1(int(2**63-1))
    >>> results[0] == results[2] == results[3] == results[4] == float(2**63-1) / -1.0 or results
    True
    >>> results[1] == results[5] == (2**63-1) // -1 or results
    True
    >>> results = py_mix_by_neg1(int(-2**63-1))
    >>> results[0] == results[2] == results[3] == results[4] == float(-2**63-1) / -1.0 or results
    True
    >>> results[1] == results[5] == (-2**63-1) // -1 or results
    True
    """
    return a/-1, a//-1, a/-1.0, a//-1.0, a/-1, a//-1


def py_mix_rev(a):
    """
    >>> py_mix_rev(4)
    (0.25, 0, 1.25, 1.0, 1.25, 1)
    >>> py_mix_rev(4.0)
    (0.25, 0.0, 1.25, 1.0, 1.25, 1.0)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def int_mix(int a):
    """
    >>> int_mix(1)
    (0.5, 0, 0.5, 0.0, 0.5, 0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def int_mix_rev(int a):
    """
    >>> int_mix_rev(4)
    (0.25, 0, 1.25, 1.0, 1.25, 1)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def float_mix(float a):
    """
    >>> float_mix(1.0)
    (0.5, 0.0, 0.5, 0.0, 0.5, 0.0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def float_mix_rev(float a):
    """
    >>> float_mix_rev(4.0)
    (0.25, 0.0, 1.25, 1.0, 1.25, 1.0)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a


def infer_division_type():
    """
    >>> v = infer_division_type()
    double
    >>> v
    8333333.25
    """
    v = (10000**2 - 1) / 12
    print(cython.typeof(v))
    return v

def int_int(int a, int b):
    """
    >>> int_int(1, 2)
    (0.5, 2.0)
    """
    return a/b, b/a


def div_by_0(a):
    """
    >>> div_by_0(0)
    'OK'
    >>> div_by_0(0.0)
    'OK'
    """
    try:
        1/a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 1"
    try:
        1//a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 2"
    try:
        5.0/a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 3"
    try:
        5.0//a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 4"
    try:
        5/a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 5"
    try:
        5//a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 6"
    try:
        (2**15)/a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 7"
    try:
        (2**15)//a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 8"
    try:
        (2**30)/a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 9"
    try:
        (2**30)//a
    except ZeroDivisionError:
        pass
    else:
        return "FAIL 10"
    return 'OK'
