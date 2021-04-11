# ticket: t676
# tag: cpp

from cython cimport typeof

cdef extern from "arithmetic_analyse_types_helper.h":
    cdef struct short_return:
        char *msg
    cdef struct int_return:
        char *msg
    cdef struct longlong_return:
        char *msg
    cdef short_return f(short)
    cdef int_return f(int)
    cdef longlong_return f(long long)

def short_binop(short val):
    """
    Arithmetic in C is always done with at least int precision.
    
    >>> print(short_binop(3))
    int called
    """
    assert typeof(val + val) == "int", typeof(val + val)
    assert typeof(val - val) == "int", typeof(val - val)
    assert typeof(val & val) == "int", typeof(val & val)
    cdef int_return x = f(val + val)
    return x.msg.decode('ASCII')

def short_unnop(short val):
    """
    Arithmetic in C is always done with at least int precision.
    
    >>> print(short_unnop(3))
    int called
    """
    cdef int_return x = f(-val)
    return x.msg.decode('ASCII')

def longlong_binop(long long val):
    """
    >>> print(longlong_binop(3))
    long long called
    """
    cdef longlong_return x = f(val * val)
    return x.msg.decode('ASCII')

def longlong_unnop(long long val):
    """
    >>> print(longlong_unnop(3))
    long long called
    """
    cdef longlong_return x = f(~val)
    return x.msg.decode('ASCII')


def test_bint(bint a):
    """
    >>> test_bint(True)
    """
    assert typeof(a + a) == "int", typeof(a + a)
    assert typeof(a & a) == "bint", typeof(a & a)
