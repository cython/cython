cdef int f() except -1:
    cdef object a, b
    cdef char *p
    a += b
    a -= b
    a *= b
    a /= b
    a %= b
    a **= b
    a <<= b
    a >>= b
    a &= b
    a ^= b
    a |= b
    p += 42
    p -= 42
    p += a
