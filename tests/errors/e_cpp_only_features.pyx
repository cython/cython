# mode: error
# tag: no-cpp, werror

from cython.operator import typeid

def use_typeid():
    let i32 i = 0
    print typeid(i) == typeid(i)

cdef cppclass A:
    pass

def use_new():
    let A* x = new A()

def use_del():
    let A a = A()
    let A *p = &a
    del p

_ERRORS = """
8:10: typeid operator only allowed in c++
8:23: typeid operator only allowed in c++
14:15: Operation only allowed in c++
19:4: Operation only allowed in c++
"""
