# mode: error

cdef struct S:
    int m

def f(a):
    cdef int i, x[2]
    cdef S s
    global j
    del f() # error
    del i # error: deletion of non-Python object
    del j # error: deletion of non-Python object
    del x[i] # error: deletion of non-Python object
    del s.m # error: deletion of non-Python object

def outer(a):
    def inner():
        print a
    del a
    return inner()


_ERRORS = u"""
10:9: Cannot assign to or delete this
11:48: Deletion of non-Python, non-C++ object
13:9: Deletion of non-Python, non-C++ object
14:9: Deletion of non-Python, non-C++ object
19:9: can not delete variable 'a' referenced in nested scope
"""
