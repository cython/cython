# mode: error

cimport cython

def closure(cython.integral i):
    def inner(cython.floating f):
        pass

def closure2(cython.integral i):
    return lambda cython.integral i: i

def closure3(cython.integral i):
    def inner():
        return lambda cython.floating f: f


_ERRORS = u"""
e_fused_closure.pyx:6:4: Cannot nest fused functions
e_fused_closure.pyx:10:11: Cannot nest fused functions
e_fused_closure.pyx:14:15: Cannot nest fused functions
"""
