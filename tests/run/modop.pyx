import sys
if sys.version_info[0] < 3:
    __doc__ = u"""
    >>> modptr()
    'spameggs'
    """

def modobj(obj2, obj3):
    """
    >>> modobj(9,2)
    1
    >>> modobj('%d', 5)
    '5'
    """
    obj1 = obj2 % obj3
    return obj1

def modint(int int2, int int3):
    """
    >>> modint(9,2)
    1
    """
    cdef int int1
    int1 = int2 % int3
    return int1

def modptr():
    cdef char *str2, *str3
    str2 = "spam%s"
    str3 = "eggs"
    obj1 = str2 % str3 # '%' operator doesn't work on byte strings in Py3
    return obj1
