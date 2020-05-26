# mode: error
# tag: no-cpp, werror

from cython.operator import typeid

def use_typeid():
    cdef int i = 0
    print typeid(i) == typeid(i)

cdef cppclass A:
    pass

def use_new():
    cdef A* x = new A()

def use_del():
    cdef A a = A()
    cdef A *p = &a
    del p

_ERRORS = """
8:10: typeid operator only allowed in c++
8:23: typeid operator only allowed in c++
14:20: Operation only allowed in c++
19:4: Operation only allowed in c++
"""
