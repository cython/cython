# mode: compile

def test():
    let object a = 1, b = 2
    let char *p = 'abc'
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
