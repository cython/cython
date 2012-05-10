# cython: binding=True
# mode: run
# tag: cyfunction

cimport cython
import sys

def get_defaults(func):
    if sys.version_info >= (2, 6, 0):
        return func.__defaults__
    return func.func_defaults

def test_defaults_none():
    """
    >>> get_defaults(test_defaults_none)
    """

def test_defaults_literal(a=1, b=(1,2,3)):
    """
    >>> get_defaults(test_defaults_literal) is get_defaults(test_defaults_literal)
    True
    >>> get_defaults(test_defaults_literal)
    (1, (1, 2, 3))
    >>> a, b = get_defaults(test_defaults_literal)
    >>> c, d = test_defaults_literal()
    >>> a is c
    True
    >>> b is d
    True
    """
    return a, b

def test_defaults_nonliteral():
    """
    >>> f0, f1 = test_defaults_nonliteral()
    >>> get_defaults(f0) is get_defaults(f0) # cached
    True
    >>> get_defaults(f0)
    (0, {}, (1, 2, 3))
    >>> a, b = get_defaults(f0)[1:]
    >>> c, d = f0(0)
    >>> a is c
    True
    >>> b is d
    True
    >>> get_defaults(f1) is get_defaults(f1) # cached
    True
    >>> get_defaults(f1)
    (0, [], (1, 2, 3))
    >>> a, b = get_defaults(f1)[1:]
    >>> c, d = f1(0)
    >>> a is c
    True
    >>> b is d
    True
    """
    ret = []
    for i in {}, []:
        def foo(a, b=0, c=i, d=(1,2,3)):
            return c, d
        ret.append(foo)
    return ret

_counter = 0
def counter():
    global _counter
    _counter += 1
    return _counter

def test_defaults_nonliteral_func_call(f):
    """
    >>> f = test_defaults_nonliteral_func_call(counter)
    >>> f()
    1
    >>> get_defaults(f)
    (1,)
    >>> f = test_defaults_nonliteral_func_call(lambda: list())
    >>> f()
    []
    >>> get_defaults(f)
    ([],)
    >>> get_defaults(f)[0] is f()
    True
    """
    def func(a=f()):
        return a
    return func

_counter2 = 1.0
def counter2():
    global _counter2
    _counter2 += 1.0
    return _counter2

def test_defaults_fused(cython.floating arg1, cython.floating arg2 = counter2()):
    """
    >>> test_defaults_fused(1.0)
    1.0 2.0
    >>> test_defaults_fused(1.0, 3.0)
    1.0 3.0
    >>> _counter2
    2.0

    >>> get_defaults(test_defaults_fused)
    (2.0,)
    >>> get_defaults(test_defaults_fused[float])
    (2.0,)
    """
    print arg1, arg2

funcs = []
for i in range(10):
    def defaults_fused(cython.floating a, cython.floating b = i):
        return a, b
    funcs.append(defaults_fused)

def test_dynamic_defaults_fused():
    """
    >>> test_dynamic_defaults_fused()
    i 0 func result (1.0, 0.0) defaults (0,)
    i 1 func result (1.0, 1.0) defaults (1,)
    i 2 func result (1.0, 2.0) defaults (2,)
    i 3 func result (1.0, 3.0) defaults (3,)
    i 4 func result (1.0, 4.0) defaults (4,)
    i 5 func result (1.0, 5.0) defaults (5,)
    i 6 func result (1.0, 6.0) defaults (6,)
    i 7 func result (1.0, 7.0) defaults (7,)
    i 8 func result (1.0, 8.0) defaults (8,)
    i 9 func result (1.0, 9.0) defaults (9,)
    """
    for i, f in enumerate(funcs):
        print "i", i, "func result", f(1.0), "defaults", get_defaults(f)

