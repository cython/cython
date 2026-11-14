# mode: error

cdef bint equal(int[:] a, int[:] b):
    return a[:5] == b[:5]

cdef bint different(int[:] a, double[:] b):
    return a != b

cdef bint ordered(int[:] a, int[:] b):
    return a < b

cdef bint identity(int[:] a, int[:] b):
    return a is b

cdef bint chained(int[:] a, int[:] b, int[:] c):
    return a == b == c

_ERRORS = u"""
4:17: Invalid types for '==' (int[:], int[:])
7:13: Invalid types for '!=' (int[:], double[:])
10:13: Invalid types for '<' (int[:], int[:])
13:13: Invalid types for 'is' (int[:], int[:])
16:13: Invalid types for '==' (int[:], int[:])
"""
