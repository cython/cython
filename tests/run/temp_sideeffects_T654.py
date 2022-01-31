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

def test_modifies_function():
    """
    >>> test_modifies_function()
    2
    """
    def inner(a):
        return a
    def get_a():
        nonlocal inner
        inner = lambda a: a*2
        return 2
    return inner(get_a())

Y = cython.declare(object, "a")
class UsesProperty(object):
    @property
    def prop(self):
        global Y
        Y = "b"
        return "c"

def reset_Y():
    global Y
    Y = "a"

def test_uses_property(reverse):
    """
    >>> test_uses_property(False)
    'cb'
    >>> reset_Y()
    >>> test_uses_property(True)
    'ac'
    """
    if reverse:
        return Y + UsesProperty().prop
    else:
        return UsesProperty().prop + Y

Z = cython.declare(object, 1)

def reset_Z():
    global Z
    Z = 1

class NonObviousAdd(object):
    def __add__(self, other):
        global Z
        Z = 2
        return other

def test_nonobvious_add(reverse):
    """
    >>> test_nonobvious_add(False)
    4
    >>> reset_Z()
    >>> test_nonobvious_add(True)
    3
    """
    if reverse:
        return Z + (NonObviousAdd() + 2)
    else:
        return (NonObviousAdd() + 2) + Z
