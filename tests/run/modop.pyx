__doc__ = """
    >>> modobj(9,2)
    1
    >>> modobj('%d', 5)
    '5'

    >>> modint(9,2)
    1
"""

def modobj(obj2, obj3):
    obj1 = obj2 % obj3
    return obj1

def modint(int int2, int int3):
    cdef int int1
    int1 = int2 % int3
    return int1

cdef modptr():
    # FIXME!!!
    cdef char *str2, *str3
    str2 = "spam"
    str3 = "eggs"

    obj1 = str2 % str3
    return obj1
