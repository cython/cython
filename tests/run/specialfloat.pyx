DEF FLOAT = 12.5
DEF EMFLOAT = 5e-1
DEF EPFLOAT = 5e+1
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
    cdef float f = FLOAT
    cdef object o = FLOAT
    assert f == o
    return f

def emfloat():
    """
    >>> emfloat()
    0.5
    """
    cdef float f = EMFLOAT
    assert f == 5e-1
    cdef object o = EMFLOAT
    assert o == 5e-1
    assert f == o
    return f

def epfloat():
    """
    >>> epfloat()
    50.0
    """
    cdef float f = EPFLOAT
    assert f == 5e+1
    cdef object o = EPFLOAT
    assert o == 5e+1
    assert f == o
    return f

def nan1():
    """
    >>> nan1()
    nan
    """
    cdef double f = FLOAT_NAN
    cdef object o = FLOAT_NAN
    assert str(f) == str(o)
    return f

def nan2():
    """
    >>> nan2()
    nan
    """
    cdef double f = float('nan')
    cdef object o = float('nan')
    assert str(f) == str(o)
    return f

def nan3():
    """
    >>> nan3()
    nan
    >>> float_nan
    nan
    """
    cdef float f = FLOAT_NAN
    cdef object o = FLOAT_NAN
    assert str(f) == str(o)
    return f

def infp1():
    """
    >>> infp1()
    inf
    >>> infp1() == float('inf')
    True
    """
    cdef double f = FLOAT_INFP
    cdef object o = FLOAT_INFP
    assert f == o
    return f

def infp2():
    """
    >>> infp2()
    inf
    >>> infp2() == float('inf')
    True
    """
    cdef double f = float('+inf')
    cdef object o = float('+inf')
    assert f == o
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
    cdef float f = FLOAT_INFP
    cdef object o = FLOAT_INFP
    assert f == o
    return f

def infn1():
    """
    >>> infn1()
    -inf
    >>> infn1() == float('-inf')
    True
    """
    cdef double f = FLOAT_INFN
    cdef object o = FLOAT_INFN
    assert f == o
    return f

def infn2():
    """
    >>> infn2()
    -inf
    >>> infn2() == float('-inf')
    True
    """
    cdef double f = float('-inf')
    cdef object o = float('-inf')
    assert f == o
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
    cdef float f = FLOAT_INFN
    cdef object o = FLOAT_INFN
    assert f == o
    return f

def global_floats():
    """
    >>> global_floats()[1:] == (float('+inf'), float('-inf'))
    True
    >>> global_floats()[0]
    nan
    """
    return (cdef_float_nan, cdef_float_infp, cdef_float_infn)
