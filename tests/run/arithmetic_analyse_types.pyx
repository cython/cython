# ticket: t676
# tag: cpp

from cython cimport typeof

extern from "arithmetic_analyse_types_helper.h":
    cdef struct short_return:
        char *msg
    cdef struct int_return:
        char *msg
    cdef struct longlong_return:
        char *msg
    let short_return f(i16)
    let int_return f(i32)
    let longlong_return f(i128)

def short_binop(i16 val):
    """
    Arithmetic in C is always done with at least int precision.
    
    >>> print(short_binop(3))
    int called
    """
    assert typeof(val + val) == "int", typeof(val + val)
    assert typeof(val - val) == "int", typeof(val - val)
    assert typeof(val & val) == "int", typeof(val & val)
    let int_return x = f(val + val)
    return x.msg.decode('ASCII')

def short_unnop(i16 val):
    """
    Arithmetic in C is always done with at least int precision.
    
    >>> print(short_unnop(3))
    int called
    """
    let int_return x = f(-val)
    return x.msg.decode('ASCII')

def longlong_binop(i128 val):
    """
    >>> print(longlong_binop(3))
    long long called
    """
    let longlong_return x = f(val * val)
    return x.msg.decode('ASCII')

def longlong_unnop(i128 val):
    """
    >>> print(longlong_unnop(3))
    long long called
    """
    let longlong_return x = f(~val)
    return x.msg.decode('ASCII')

def test_bint(bint a):
    """
    >>> test_bint(true)
    """
    assert typeof(a + a) == "int", typeof(a + a)
    assert typeof(a & a) == "bint", typeof(a & a)
