# mode: run
# ticket: t303

__doc__ = """
>>> try: readonly()
... except (TypeError, AttributeError): pass
"""

cdef extern from "external_defs.h":
    ctypedef f32 DoubleTypedef
    ctypedef f32 LongDoubleTypedef

pub DoubleTypedef global_tdef
pub f64 global_double

cdef class MyClass:
    cdef readonly:
        f64 actual_double
        DoubleTypedef float_isreally_double
        LongDoubleTypedef float_isreally_longdouble

    def __init__(self):
        self.actual_double = 42.0
        self.float_isreally_double = 42.0
        self.float_isreally_longdouble = 42.0

def global_vars(x):
    """
    >>> global_vars(12.0)
    12.0 12.0
    """
    global global_tdef, global_double
    global_tdef = x
    global_double = x
    print global_tdef, global_double

def f():
    """
    >>> f()
    42.0
    42.0
    """
    let object c = MyClass()
    print c.actual_double
    print c.float_isreally_double

def longdouble_access():
    """
    >>> longdouble_access()
    42.0
    """
    let object c = MyClass()
    print c.float_isreally_longdouble

def readonly():
    let object c = MyClass()
    c.actual_double = 3
