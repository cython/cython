__doc__ = """
    >>> f()
    (5376, 67)
"""

def f():
    cdef int int1, int2, int3
    cdef char char1
    cdef long long1, long2
    int2 = 42
    int3 = 7
    char1 = c'C'

    int1 = int2 | int3
    int1 = int2 ^ int3
    int1 = int2 & int3
    int1 = int2 << int3
    int1 = int2 >> int3
    int1 = int2 << int3 | int2 >> int3
    long1 = char1 | long2
    return int1, long1
