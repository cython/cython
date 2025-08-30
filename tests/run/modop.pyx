import sys


def modobj(obj2, obj3):
    """
    >>> modobj(9,2)
    1
    >>> modobj('%d', 5)
    '5'
    >>> modobj(1, 0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ... by zero
    """
    obj1 = obj2 % obj3
    return obj1


def mod_10_obj(int2):
    """
    >>> mod_10_obj(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ... by zero
    >>> 10 % 1
    0
    >>> mod_10_obj(1)
    0
    >>> mod_10_obj(3)
    1
    >>> 10 % -1
    0
    >>> mod_10_obj(-1)
    0
    >>> mod_10_obj(-10)
    0
    """
    int1 = 10 % int2
    return int1


def mod_obj_10(int2):
    """
    >>> 0 % 10
    0
    >>> mod_obj_10(0)
    0
    >>> 1 % 10
    1
    >>> mod_obj_10(1)
    1
    >>> (-1) % 10
    9
    >>> mod_obj_10(-1)
    9
    >>> 9 % 10
    9
    >>> mod_obj_10(9)
    9
    >>> 10 % 10
    0
    >>> mod_obj_10(10)
    0
    >>> (-10) % 10
    0
    >>> mod_obj_10(-10)
    0
    >>> (-12) % 10
    8
    >>> mod_obj_10(-12)
    8
    >>> 10002 % 10
    2
    >>> mod_obj_10(10002)
    2
    >>> int((2**25) % 10)
    2
    >>> int(mod_obj_10(2**25))
    2
    >>> int((-2**25) % 10)
    8
    >>> int(mod_obj_10(-2**25))
    8
    >>> int((-2**31-1) % 10)
    1
    >>> int(mod_obj_10(int(-2**31-1)))
    1
    >>> int((2**50) % 10)
    4
    >>> int(mod_obj_10(2**50))
    4
    >>> int((-2**50) % 10)
    6
    >>> int(mod_obj_10(-2**50))
    6
    >>> int((-2**63-1) % 10)
    1
    >>> int(mod_obj_10(-2**63-1))
    1
    >>> int((2**200) % 10)
    6
    >>> int(mod_obj_10(2**200))
    6
    >>> int((-2**200) % 10)
    4
    >>> int(mod_obj_10(-2**200))
    4
    """
    int1 = int2 % 10
    return int1


def mod_obj_17(int2):
    """
    >>> 0 % 17
    0
    >>> mod_obj_17(0)
    0
    >>> 1 % 17
    1
    >>> mod_obj_17(1)
    1
    >>> (-1) % 17
    16
    >>> mod_obj_17(-1)
    16
    >>> 9 % 17
    9
    >>> mod_obj_17(16)
    16
    >>> 17 % 17
    0
    >>> mod_obj_17(17)
    0
    >>> (-17) % 17
    0
    >>> mod_obj_17(-17)
    0
    >>> (-18) % 17
    16
    >>> mod_obj_17(-18)
    16
    >>> 10002 % 17
    6
    >>> mod_obj_17(10002)
    6
    >>> int((2**25) % 17)
    2
    >>> int(mod_obj_17(2**25))
    2
    >>> int((-2**25) % 17)
    15
    >>> int(mod_obj_17(-2**25))
    15
    >>> int((-2**31-1) % 17)
    7
    >>> int(mod_obj_17(int(-2**31-1)))
    7
    >>> int((2**50) % 17)
    4
    >>> int(mod_obj_17(2**50))
    4
    >>> int((-2**50) % 17)
    13
    >>> int(mod_obj_17(-2**50))
    13
    >>> int((-2**63-1) % 17)
    7
    >>> int(mod_obj_17(-2**63-1))
    7
    >>> int((2**200) % 17)
    1
    >>> int(mod_obj_17(2**200))
    1
    >>> int((-2**200) % 17)
    16
    >>> int(mod_obj_17(-2**200))
    16
    """
    int1 = int2 % 17
    return int1


def mod_int_17(int int2):
    """
    >>> 0 % 17
    0
    >>> mod_int_17(0)
    0
    >>> 1 % 17
    1
    >>> mod_int_17(1)
    1
    >>> (-1) % 17
    16
    >>> mod_int_17(-1)
    16
    >>> 9 % 17
    9
    >>> mod_int_17(16)
    16
    >>> 17 % 17
    0
    >>> mod_int_17(17)
    0
    >>> (-17) % 17
    0
    >>> mod_int_17(-17)
    0
    >>> (-18) % 17
    16
    >>> mod_int_17(-18)
    16
    >>> 10002 % 17
    6
    >>> mod_int_17(10002)
    6
    >>> int((2**25) % 17)
    2
    >>> int(mod_int_17(2**25))
    2
    >>> int((-2**25) % 17)
    15
    >>> int(mod_int_17(-2**25))
    15
    """
    int1 = int2 % 17
    return int1


def mod_obj_m2(int2):
    """
    >>> 0 % -2
    0
    >>> mod_obj_m2(0)
    0
    >>> 1 % -2
    -1
    >>> mod_obj_m2(1)
    -1
    >>> 9 % -2
    -1
    >>> mod_obj_m2(9)
    -1
    """
    int1 = int2 % -2
    return int1


def mod_obj_m2f(obj2):
    """
    >>> 0 % -2.0 == 0.0    # -0.0 in Py2.7+
    True
    >>> mod_obj_m2f(0)
    -0.0
    >>> 1 % -2.0
    -1.0
    >>> mod_obj_m2f(1)
    -1.0
    >>> 9 % -2.0
    -1.0
    >>> mod_obj_m2f(9)
    -1.0
    """
    result = obj2 % -2.0
    return result


def modint(int int2, int int3):
    """
    >>> modint(9,2)
    1
    """
    cdef int int1
    int1 = int2 % int3
    return int1


def modptr():
    """
    >>> modptr()
    b'spameggs'
    """
    cdef char *str2, *str3
    str2 = "spam%s"
    str3 = "eggs"
    obj1 = str2 % str3
    return obj1


def mod_bigint(obj):
    """
    >>> mod_bigint(3316000000000)
    319
    """
    result = obj % 999
    return result
