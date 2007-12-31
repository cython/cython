cdef class MyClass:
    pass

def foo(MyClass c):
    cdef MyClass res
    res = c
    return res
