a,b = 'a *','b *' # use non-interned strings

def and2_assign(a,b):
    """
    >>> a,b = 'a *','b *' # use non-interned strings
    >>> and2_assign(2,3) == (2 and 3)
    True
    >>> and2_assign('a', 'b') == ('a' and 'b')
    True
    >>> and2_assign(a, b) == (a and b)
    True
    """
    c = a and b
    return c

def and2(a,b):
    """
    >>> and2(2,3) == (2 and 3)
    True
    >>> and2(0,2) == (0 and 2)
    True
    >>> and2('a', 'b') == ('a' and 'b')
    True
    >>> and2(a, b) == (a and b)
    True
    >>> and2('', 'b') == ('' and 'b')
    True
    >>> and2([], [1]) == ([] and [1])
    True
    >>> and2([], [a]) == ([] and [a])
    True
    """
    return a and b

def and3(a,b,c):
    """
    >>> and3(0,1,2) == (0 and 1 and 2)
    True
    >>> and3([],(),[1]) == ([] and () and [1])
    True
    """
    d = a and b and c
    return d

def and2_no_result(a,b):
    """
    >>> and2_no_result(2,3)
    >>> and2_no_result(0,2)
    >>> and2_no_result('a','b')
    >>> and2_no_result(a,b)
    >>> a and b
    'b *'
    """
    a and b

def and2_literal():
    """
    >>> and2_literal()
    5
    """
    return True and 5

def c_int_results(int x):
    """
    >>> c_int_results(7)
    (0, 0)
    >>> c_int_results(5)
    (1, 1)
    """
    cdef int expr1, expr2, r1, r2

    expr1 = x == 5
    expr2 = 1
    r1 = expr1 and expr2

    r2 = (x==5) and 1
    return r1, r2
