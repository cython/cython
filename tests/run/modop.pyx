import sys


def modobj(obj2, obj3):
    """
    >>> modobj(9,2)
    1
    >>> modobj('%d', 5)
    '5'
    """
    obj1 = obj2 % obj3
    return obj1


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
    >>> 9 % 10
    9
    >>> mod_obj_10(9)
    9
    >>> 10 % 10
    0
    >>> mod_obj_10(10)
    0
    >>> 10002 % 10
    2
    >>> mod_obj_10(10002)
    2
    >>> int((2**50) % 10)
    4
    >>> int(mod_obj_10(2**50))
    4
    >>> int((2**200) % 10)
    6
    >>> int(mod_obj_10(2**200))
    6
    >>> (-1) % 10
    9
    >>> mod_obj_10(-1)
    9
    >>> (-10) % 10
    0
    >>> mod_obj_10(-10)
    0
    >>> (-12) % 10
    8
    >>> mod_obj_10(-12)
    8
    """
    int1 = int2 % 10
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
    >>> print(modptr() if sys.version_info[0] < 3 else 'spameggs')
    spameggs
    """
    cdef char *str2, *str3
    str2 = "spam%s"
    str3 = "eggs"
    obj1 = str2 % str3  # '%' operator doesn't work on byte strings in Py3
    return obj1
