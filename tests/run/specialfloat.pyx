__doc__ = """
    >>> f()
    12.5

    >>> nan1()
    nan
    >>> nan2()
    nan
    >>> float_nan
    nan

    >>> infp1()
    inf
    >>> infp1() == float('inf')
    True
    >>> infp2()
    inf
    >>> infp2() == float('inf')
    True
    >>> float_infp
    inf
    >>> float_infp == float('inf')
    True

    >>> infn1()
    -inf
    >>> infn1() == float('-inf')
    True
    >>> infn2()
    -inf
    >>> infn2() == float('-inf')
    True
    >>> float_infn
    -inf
    >>> float_infn == float('-inf')
    True
"""

DEF FLOAT = 12.5
DEF FLOAT_NAN = float('nan')
DEF FLOAT_INFP = float('+inf')
DEF FLOAT_INFN = float('-inf')

float_nan = FLOAT_NAN
float_infp = FLOAT_INFP
float_infn = FLOAT_INFN

def f():
    cdef float f
    f = FLOAT
    return f

def nan1():
    cdef double f
    f = FLOAT_NAN
    return f

def nan2():
    cdef double f
    f = float('nan')
    return f

def infp1():
    cdef double f
    f = FLOAT_INFP
    return f

def infp2():
    cdef double f
    f = float('+inf')
    return f

def infn1():
    cdef double f
    f = FLOAT_INFN
    return f

def infn2():
    cdef double f
    f = float('-inf')
    return f

