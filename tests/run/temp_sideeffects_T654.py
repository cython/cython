# ticket: t654
# tag pure3.7

# function call arguments

# not really a bug, Cython warns about it now -- C argument evaluation order is undefined
# however, Cython does try to ensure that name/attribute lookups aren't
# affected by the evaluation order

import cython

# module globals

X = cython.declare(object, 1)
@cython.cfunc
def redefine_global():
    global X
    x,X = X,2
    return x

@cython.cfunc
@cython.locals(o=cython.int)
def call3(x1, o, x2):
    return (x1, o, x2)

def test_global_redefine():
    """
    >>> test_global_redefine()
    (1, 1, 2)
    """
    return call3(X, redefine_global(), X)

def test_nonlocal_redefine(x):
    """
    >>> test_nonlocal_redefine(5)
    15
    """
    def inner():
        nonlocal x
        x *= 2
        return x
    return x+inner()

def test_assignment_expression(x):
    """
    >>> test_assignment_expression(5)
    15
    """
    return x+(x:=x*2)

@cython.cclass
class C:
    x: object
    def __init__(self):
        self.x = 1

def test_nonlocal_attr():
    """
    >>> test_nonlocal_attr()
    4
    """
    c: C = C()
    def inner():
        nonlocal c
        c.x = 2
        return 3
    return c.x+inner()
