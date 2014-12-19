# mode: compile

def test():
    cdef object a = 1, b = 2
    cdef char *p = 'abc'
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
