__doc__ = u"""
    >>> int2 = 42
    >>> int3 = 7
    >>> char1 = ord('C')

    >>> int1 = int2 | int3
    >>> int1 |= int2 ^ int3
    >>> int1 ^= int2 & int3
    >>> int1 ^= int2 << int3
    >>> int1 ^= int2 >> int3
    >>> int1 ^= int2 << int3 | int2 >> int3
    >>> long1 = char1 | int1
    >>> print (int1, long1) == f()
    True

    >>> f()
    (45, 111)
"""

def f():
    cdef int int1, int2, int3
    cdef char char1
    cdef long long1, long2
    int2 = 42
    int3 = 7
    char1 = c'C'

    int1 = int2 | int3
    int1 |= int2 ^ int3
    int1 ^= int2 & int3
    int1 ^= int2 << int3
    int1 ^= int2 >> int3
    int1 ^= int2 << int3 | int2 >> int3
    long1 = char1 | int1
    return int1, long1
