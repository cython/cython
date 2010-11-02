__doc__ = u"""
#>>> py_identity = lambda x:x
#>>> py_identity(1) == cy_identity(1)
#True
"""

#cy_identity = lambda x:x


def make_identity():
    """
    >>> idcall = make_identity()
    >>> idcall(1)
    1
    >>> idcall(2)
    2
    """
    return lambda x:x

def make_const0(x):
    """
    >>> make_const0(1)()
    1
    """
    return lambda :x

def make_const1(x):
    """
    >>> make_const1(1)(2)
    1
    >>> make_const1(1)(2)
    1
    """
    return lambda _:x


def make_const_calc0():
    """
    >>> make_const_calc0()()
    11
    """
    return lambda : 1*2*3+5

def make_const_calc1():
    """
    >>> make_const_calc1()(2)
    11
    """
    return lambda _: 1*2*3+5

def make_const_calc1_xy(x):
    """
    >>> make_const_calc1_xy(8)(2)
    27
    """
    return lambda y: x*y+(1*2*3+5)

def make_lambda_lambda(x):
    """
    >>> make_lambda_lambda(1)(2)(4)
    7
    """
    return lambda y : \
           lambda z:x+y+z

def make_typed_lambda_lambda(int x):
    """
    >>> make_typed_lambda_lambda(1)(2)(4)
    7

    >>> partial_lambda = make_typed_lambda_lambda(1)(2)
    >>> partial_lambda(4)
    7
    >>> partial_lambda(5)
    8
    """
    return lambda int y : \
           lambda int z:x+y+z
