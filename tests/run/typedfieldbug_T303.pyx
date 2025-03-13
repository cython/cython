# mode: run
# ticket: t303

__doc__ = """
>>> try: readonly()
... except (TypeError, AttributeError): pass
"""


cdef extern from "external_defs.h":
    ctypedef float DoubleTypedef
    ctypedef float LongDoubleTypedef

cdef public DoubleTypedef global_tdef
cdef public double global_double

cdef class MyClass:
    cdef readonly:
        double actual_double
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
    cdef object c = MyClass()
    print c.actual_double
    print c.float_isreally_double

def longdouble_access():
    """
    >>> longdouble_access()
    42.0
    """
    cdef object c = MyClass()
    print c.float_isreally_longdouble


def readonly():
    cdef object c = MyClass()
    c.actual_double = 3
