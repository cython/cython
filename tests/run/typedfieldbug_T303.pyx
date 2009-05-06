"""
>>> f()
42.0 42.0
"""

cdef extern from "external_defs.h":
    ctypedef float DoubleTypedef

cdef class MyClass:
    cdef readonly:
        double var_d
        DoubleTypedef var_nf
    def __init__(self):
        self.var_d = 42.0
        self.var_nf = 42.0

def f():
    c = MyClass()
    print c.var_d, c.var_nf

