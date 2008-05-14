__doc__ = u"""
>>> f(100)
101
>>> g(3000000000)
3000000001
"""

def f(x):
    cdef unsigned long long ull
    ull = x
    return ull + 1

def g(unsigned long x):
    return x + 1
