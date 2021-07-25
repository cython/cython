# mode: run
# tag: condexpr
# ticket: t267

cimport cython

def ident(x): return x

def constants(x):
    """
    >>> constants(4)
    1
    >>> constants(5)
    10
    """
    a = 1 if x < 5 else 10
    return a

def temps(x):
    """
    >>> temps(4)
    1
    >>> temps(5)
    10
    """
    return ident(1) if ident(x) < ident(5) else ident(10)


def nested(x):
    """
    >>> nested(1)
    1
    >>> nested(2)
    2
    >>> nested(3)
    3
    """
    a = 1 if x == 1 else (2 if x == 2 else 3)
    return a


@cython.test_fail_if_path_exists('//CondExprNode')
def const_true(a,b):
    """
    >>> const_true(1,2)
    1
    """
    return a if 1 == 1 else b

@cython.test_fail_if_path_exists('//CondExprNode')
def const_false(a,b):
    """
    >>> const_false(1,2)
    2
    """
    return a if 1 != 1 else b
