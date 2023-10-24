# mode: error

struct S:
    i32 m

def f(a):
    let i32 i, x[2]
    let S s
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

cdef object g
del g


_ERRORS = u"""
10:9: Cannot assign to or delete this
11:8: Deletion of non-Python, non-C++ object
13:9: Deletion of non-Python, non-C++ object
14:9: Deletion of non-Python, non-C++ object
19:8: can not delete variable 'a' referenced in nested scope
23:4: Deletion of global C variable
"""
