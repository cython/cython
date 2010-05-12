DEF FLOAT = 12.5
DEF EFLOAT = 5e-1
DEF FLOAT_NAN = float('nan')
DEF FLOAT_INFP = float('+inf')
DEF FLOAT_INFN = float('-inf')

cdef double cdef_float_nan = float('nan')
cdef double cdef_float_infp = float('+inf')
cdef double cdef_float_infn = float('-inf')

float_nan = FLOAT_NAN
float_infp = FLOAT_INFP
float_infn = FLOAT_INFN

def f():
    """
    >>> f()
    12.5
    """
    cdef float f
    f = FLOAT
    return f

def efloat():
    """
    >>> efloat()
    0.5
    """
    cdef float f = EFLOAT
    return f

def nan1():
    """
    >>> nan1()
    nan
    """
    cdef double f
    f = FLOAT_NAN
    return f

def nan2():
    """
    >>> nan2()
    nan
    """
    cdef double f
    f = float('nan')
    return f

def nan3():
    """
    >>> nan3()
    nan
    >>> float_nan
    nan
    """
    cdef float f
    f = FLOAT_NAN
    return f

def infp1():
    """
    >>> infp1()
    inf
    >>> infp1() == float('inf')
    True
    """
    cdef double f
    f = FLOAT_INFP
    return f

def infp2():
    """
    >>> infp2()
    inf
    >>> infp2() == float('inf')
    True
    """
    cdef double f
    f = float('+inf')
    return f

def infp3():
    """
    >>> infp3()
    inf
    >>> infp3() == float('inf')
    True
    >>> float_infp
    inf
    >>> float_infp == float('inf')
    True
    """
    cdef float f
    f = FLOAT_INFP
    return f

def infn1():
    """
    >>> infn1()
    -inf
    >>> infn1() == float('-inf')
    True
    """
    cdef double f
    f = FLOAT_INFN
    return f

def infn2():
    """
    >>> infn2()
    -inf
    >>> infn2() == float('-inf')
    True
    """
    cdef double f
    f = float('-inf')
    return f

def infn3():
    """
    >>> infn3()
    -inf
    >>> infn3() == float('-inf')
    True
    >>> float_infn
    -inf
    >>> float_infn == float('-inf')
    True
    """
    cdef float f
    f = FLOAT_INFN
    return f

def global_floats():
    """
    >>> global_floats()[1:] == (float('+inf'), float('-inf'))
    True
    >>> global_floats()[0]
    nan
    """
    return (cdef_float_nan, cdef_float_infp, cdef_float_infn)
