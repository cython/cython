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
    let f32 f = FLOAT
    let object o = FLOAT
    assert f == o
    return f

def emfloat():
    """
    >>> emfloat()
    0.5
    """
    let f32 f = EMFLOAT
    assert f == 5e-1
    let object o = EMFLOAT
    assert o == 5e-1
    assert f == o
    return f

def epfloat():
    """
    >>> epfloat()
    50.0
    """
    let f32 f = EPFLOAT
    assert f == 5e+1
    let object o = EPFLOAT
    assert o == 5e+1
    assert f == o
    return f

def nan1():
    """
    >>> nan1()
    nan
    """
    let f64 f = FLOAT_NAN
    let object o = FLOAT_NAN
    assert str(f) == str(o)
    return f

def nan2():
    """
    >>> nan2()
    nan
    """
    let f64 f = float('nan')
    let object o = float('nan')
    assert str(f) == str(o)
    return f

def nan3():
    """
    >>> nan3()
    nan
    >>> float_nan
    nan
    """
    let f32 f = FLOAT_NAN
    let object o = FLOAT_NAN
    assert str(f) == str(o)
    return f

def infp1():
    """
    >>> infp1()
    inf
    >>> infp1() == float('inf')
    True
    """
    let f64 f = FLOAT_INFP
    let object o = FLOAT_INFP
    assert f == o
    return f

def infp2():
    """
    >>> infp2()
    inf
    >>> infp2() == float('inf')
    True
    """
    let f64 f = float('+inf')
    let object o = float('+inf')
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
    let f32 f = FLOAT_INFP
    let object o = FLOAT_INFP
    assert f == o
    return f

def infn1():
    """
    >>> infn1()
    -inf
    >>> infn1() == float('-inf')
    True
    """
    let f64 f = FLOAT_INFN
    let object o = FLOAT_INFN
    assert f == o
    return f

def infn2():
    """
    >>> infn2()
    -inf
    >>> infn2() == float('-inf')
    True
    """
    let f64 f = float('-inf')
    let object o = float('-inf')
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
    let f32 f = FLOAT_INFN
    let object o = FLOAT_INFN
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
