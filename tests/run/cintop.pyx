# mode: run

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
    >>> (int1, long1) == f()
    True

"""

def f():
    """
    >>> f()
    (45, 111)
    """
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


def long_int_shift():
    """
    >>> long_int_shift()
    80082
    10010
    10010
    10010
    10010
    """
    value = 80082 # int using more than 2 bytes == long
    print(value)
    shiftedby3 = value >> 3
    dividedby8 = value // 8
    print(shiftedby3)
    print(dividedby8)
    shiftedby3 = 80082 >> 3
    dividedby8 = 80082 // 8
    print(shiftedby3)
    print(dividedby8)
