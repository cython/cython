# cython: warn.undeclared=True
# mode: error
# tag: werror

def foo():
    a = 1
    return a

cdef class Bar:
    cdef int baz(self, a):
        res = 0
        for i in range(3):
            res += i
        return res

_ERRORS = """
6:4: implicit declaration of 'a'
11:8: implicit declaration of 'res'
12:12: implicit declaration of 'i'
"""
