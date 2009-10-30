import cython

def test_sizeof():
    """
    >>> test_sizeof()
    True
    True
    True
    True
    True
    """
    x = cython.declare(cython.bint)
    print sizeof(x) == sizeof(cython.bint)
    print sizeof(cython.char) <= sizeof(cython.short) <= sizeof(cython.int) <= sizeof(cython.long) <= sizeof(cython.longlong)
    print sizeof(cython.uint) == sizeof(cython.int)
    print sizeof(cython.p_int) == sizeof(cython.p_double)
    if cython.compiled:
        print sizeof(cython.char) < sizeof(cython.longlong)
    else:
        print sizeof(cython.char) == 1

def test_declare(n):
    """
    >>> test_declare(100)
    (100, 100)
    >>> test_declare(100.5)
    (100, 100)
    >>> test_declare(None)
    Traceback (most recent call last):
    ...
    TypeError: an integer is required
    """
    x = cython.declare(cython.int)
    y = cython.declare(cython.int, n)
    if cython.compiled:
        cython.declare(xx=cython.int, yy=cython.long)
        i = sizeof(xx)
    ptr = cython.declare(cython.p_int, cython.address(y))
    return y, ptr[0]
    
@cython.locals(x=cython.double, n=cython.int)
def test_cast(x):
    """
    >>> test_cast(1.5)
    1
    >>> test_cast(None)
    Traceback (most recent call last):
    ...
    TypeError: a float is required
    """
    n = cython.cast(cython.int, x)
    return n
    
@cython.locals(x=cython.int, y=cython.p_int)
def test_address(x):
    """
    >>> test_address(39)
    39
    """
    y = cython.address(x)
    return y[0]

@cython.locals(x=cython.int)
@cython.locals(y=cython.bint)
def test_locals(x):
    """
    >>> test_locals(5)
    True
    """
    y = x
    return y
    

MyUnion = cython.union(n=cython.int, x=cython.double)
MyStruct = cython.struct(is_integral=cython.bint, data=MyUnion)
MyStruct2 = cython.typedef(MyStruct[2])

def test_struct(n, x):
    """
    >>> test_struct(389, 1.64493)
    (389, 1.64493)
    """
    a = cython.declare(MyStruct2)
    a[0] = MyStruct(True, data=MyUnion(n=n))
    a[1] = MyStruct(is_integral=False, data={'x': x})
    return a[0].data.n, a[1].data.x

import cython as cy
from cython import declare, cast, locals, address, typedef, p_void, compiled
from cython import declare as my_declare, locals as my_locals, p_void as my_void_star, typedef as my_typedef, compiled as my_compiled

@my_locals(a=cython.p_void)
def test_imports():
    """
    >>> test_imports()
    True
    """
    a = cython.NULL
    b = declare(p_void, cython.NULL)
    c = my_declare(my_void_star, cython.NULL)
    d = cy.declare(cy.p_void, cython.NULL)
    return a == d and compiled and my_compiled

MyStruct3 = typedef(MyStruct[3])
MyStruct4 = my_typedef(MyStruct[4])
MyStruct5 = cy.typedef(MyStruct[5])
