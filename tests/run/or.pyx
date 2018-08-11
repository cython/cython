a,b = 'a *','b *' # use non-interned strings

def or2_assign(a,b):
    """
    >>> or2_assign(2,3) == (2 or 3)
    True
    >>> or2_assign('a', 'b') == ('a' or 'b')
    True
    >>> or2_assign(a, b) == (a or b)
    True
    """
    c = a or b
    return c

def or2(a,b):
    """
    >>> or2(2,3) == (2 or 3)
    True
    >>> or2(0,2) == (0 or 2)
    True
    >>> or2('a', 'b') == ('a' or 'b')
    True
    >>> or2(a, b) == (a or b)
    True
    >>> or2('', 'b') == ('' or 'b')
    True
    >>> or2([], [1]) == ([] or [1])
    True
    >>> or2([], [a]) == ([] or [a])
    True
    """
    return a or b

def or3(a,b,c):
    """
    >>> or3(0,1,2) == (0 or 1 or 2)
    True
    >>> or3([],(),[1]) == ([] or () or [1])
    True
    """
    d = a or b or c
    return d

def or2_no_result(a,b):
    """
    >>> or2_no_result(2,3)
    >>> or2_no_result(0,2)
    >>> or2_no_result('a','b')
    >>> or2_no_result(a,b)
    >>> a or b
    'a *'
    """
    a or b

def or2_literal():
    """
    >>> or2_literal()
    5
    """
    return False or 5

cdef class A(object):
    def __repr__(self):
        return "A"

def test_GH2059_missing_cast():
    """
    >>> test_GH2059_missing_cast()
    (A, A)
    """
    cdef A a = A()
    cdef object o = None
    cdef A a_first = a or o
    cdef A a_second = o or a
    return a_first, a_second
