# cython: binding=True
# mode: run
# tag: cyfunction, closures

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


def cy_kwonly_default_args(a, x=1, *, b=2):
    l = m = 1

def test_kwdefaults(value):
    """
    >>> cy_kwonly_default_args.__defaults__
    (1,)
    >>> cy_kwonly_default_args.func_defaults
    (1,)

    >>> cy_kwonly_default_args.__kwdefaults__
    {'b': 2}

    >>> test_kwdefaults.__defaults__
    >>> test_kwdefaults.__kwdefaults__

    >>> f = test_kwdefaults(5)
    >>> f.__defaults__
    (1,)
    >>> f.__kwdefaults__
    {'b': 5}
    >>> f.__kwdefaults__ = ()
    Traceback (most recent call last):
    TypeError: __kwdefaults__ must be set to a dict object
    >>> f.__kwdefaults__ = None
    >>> f.__kwdefaults__
    >>> f.__kwdefaults__ = {}
    >>> f.__kwdefaults__
    {}
    >>> f.__kwdefaults__ = {'a': 2}
    >>> f.__kwdefaults__
    {'a': 2}
    """
    def kwonly_default_args(a, x=1, *, b=value):
        return a, x, b
    return kwonly_default_args


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


def test_memoryview_none(const unsigned char[:] b=None):
    """
    >>> test_memoryview_none()
    >>> test_memoryview_none(None)
    >>> test_memoryview_none(b'abc')
    97
    """
    if b is None:
        return None
    return b[0]


def test_memoryview_bytes(const unsigned char[:] b=b'xyz'):
    """
    >>> test_memoryview_bytes()
    120
    >>> test_memoryview_bytes(None)
    >>> test_memoryview_bytes(b'abc')
    97
    """
    if b is None:
        return None
    return b[0]


@cython.test_fail_if_path_exists(
    '//NameNode[@entry.in_closure = True]',
    '//NameNode[@entry.from_closure = True]')
def test_func_default_inlined():
    """
    Make sure we don't accidentally generate a closure.

    >>> func = test_func_default_inlined()
    >>> func()
    1
    >>> func(2)
    2
    """
    def default():
        return 1
    def func(arg=default()):
        return arg
    return func


@cython.test_fail_if_path_exists(
    '//NameNode[@entry.in_closure = True]',
    '//NameNode[@entry.from_closure = True]')
def test_func_default_scope():
    """
    Test that the default value expression is evaluated in the outer scope.

    >>> func = test_func_default_scope()
    3
    >>> func()
    [0, 1, 2, 3]
    >>> func(2)
    2
    """
    i = -1
    def func(arg=[ i for i in range(4) ]):
        return arg
    print i  # list comps leak in Py2 mode => i == 3
    return func


def test_func_default_scope_local():
    """
    >>> func = test_func_default_scope_local()
    -1
    >>> func()
    [0, 1, 2, 3]
    >>> func(2)
    2
    """
    i = -1
    def func(arg=list(i for i in range(4))):
        return arg
    print i  # genexprs don't leak
    return func
