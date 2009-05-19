"""
>>> f()
42.0 42.0 42.0
>>> readonly()
Traceback (most recent call last):
    ...
AttributeError: attribute 'var_nf' of 'typedfieldbug_T303.MyClass' objects is not writable
"""

cdef extern from "external_defs.h":
    ctypedef float DoubleTypedef

cdef class MyClass:
    cdef readonly:
        double var_d
        DoubleTypedef var_nf
    cdef public:
        DoubleTypedef var_mutable
    def __init__(self):
        self.var_d = 42.0
        self.var_nf = 42.0
        self.var_mutable = 1

def f():
    c = MyClass()
    c.var_mutable = 42.0
    print c.var_d, c.var_nf, c.var_mutable

def readonly():
    c = MyClass()
    c.var_nf = 3
