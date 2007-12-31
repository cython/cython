__doc__ = """
print f(100)
print g(3000000000)
"""

def f(x):
    cdef unsigned long long ull
    ull = x
    return ull + 1

def g(unsigned long x):
    return x + 1
