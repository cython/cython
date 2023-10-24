# mode: error

cdef class C:
    cdef object __weakref__

cdef class D:
    pub object __weakref__

cdef class E:
    cdef readonly object __weakref__

fn void f():
    let C c = C()
    let object x
    x = c.__weakref__
    c.__weakref__ = x

_ERRORS = u"""
7:15: Illegal use of special attribute __weakref__
7:15: Illegal use of special attribute __weakref__
7:15: Illegal use of special attribute __weakref__
7:15: Special attribute __weakref__ cannot be exposed to Python
10:25: Illegal use of special attribute __weakref__
10:25: Special attribute __weakref__ cannot be exposed to Python
15:9: Illegal use of special attribute __weakref__
16:5: Illegal use of special attribute __weakref__
"""
