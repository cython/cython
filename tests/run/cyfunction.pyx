# cython: binding=True
# mode: run
# tag: cyfunction

import sys
IS_PY2 = sys.version_info[0] < 3
IS_PY3 = sys.version_info[0] >= 3
IS_PY34 = sys.version_info > (3, 4, 0, 'beta', 3)


def inspect_isroutine():
    """
    >>> inspect_isroutine()
    True
    """
    import inspect
    return inspect.isroutine(inspect_isroutine)


def inspect_isfunction():
    """
    >>> inspect_isfunction()
    False
    False
    """
    import inspect, types
    print isinstance(inspect_isfunction, types.FunctionType)
    return inspect.isfunction(inspect_isfunction)


def inspect_isbuiltin():
    """
    >>> inspect_isbuiltin()
    False
    False
    """
    import inspect, types
    print isinstance(inspect_isfunction, types.BuiltinFunctionType)
    return inspect.isbuiltin(inspect_isbuiltin)


def inspect_signature(a, b, c=123, *, d=234):
    """
    >>> sig = inspect_signature(1, 2)
    >>> if IS_PY34: list(sig.parameters)
    ... else: ['a', 'b', 'c', 'd']
    ['a', 'b', 'c', 'd']
    >>> if IS_PY34: sig.parameters['c'].default == 123
    ... else: True
    True
    >>> if IS_PY34: sig.parameters['d'].default == 234
    ... else: True
    True
    """
    import inspect
    return inspect.signature(inspect_signature) if IS_PY34 else None


# def test___signature__(a, b, c=123, *, d=234):
#     """
#     >>> sig = test___signature__(1, 2)
#     >>> if IS_PY34: list(sig.parameters)
#     ... else: ['a', 'b', 'c', 'd']
#     ['a', 'b', 'c', 'd']
#     >>> if IS_PY34: sig.parameters['c'].default == 123
#     ... else: True
#     True
#     >>> if IS_PY34: sig.parameters['d'].default == 234
#     ... else: True
#     True
#     """
#     return inspect_signature.__signature__ if IS_PY34 else None


def test_dict():
    """
    >>> test_dict.foo = 123
    >>> test_dict.__dict__
    {'foo': 123}
    >>> test_dict.__dict__ = {'bar': 321}
    >>> test_dict.__dict__
    {'bar': 321}
    >>> test_dict.func_dict
    {'bar': 321}
    """

def test_name():
    """
    >>> test_name.__name__
    'test_name'
    >>> test_name.func_name
    'test_name'
    >>> test_name.__name__ = 123 #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: __name__ must be set to a ... object
    >>> test_name.__name__ = 'foo'
    >>> test_name.__name__
    'foo'
    """

def test_doc():
    """
    >>> del test_doc.__doc__
    >>> test_doc.__doc__
    >>> test_doc.__doc__ = 'docstring'
    >>> test_doc.__doc__
    'docstring'
    >>> test_doc.func_doc
    'docstring'
    """


def test_hash():
    """
    >>> d = {test_hash: 123}
    >>> test_hash in d
    True
    >>> d[test_hash]
    123
    >>> hash(test_hash) == hash(test_hash)
    True
    """


def test_closure():
    """
    >>> test_closure.func_closure is None
    True
    """

def test_globals():
    """
    >>> test_globals.func_globals is not None
    True
    >>> 'test_globals' in test_globals.func_globals or test_globals.func_globals
    True
    >>> 'test_name' in test_globals.func_globals or test_globals.func_globals
    True
    >>> 'not there' not in test_globals.func_globals or test_globals.func_globals
    True
    >>> try: test_globals.func_globals = {}
    ... except (AttributeError, TypeError): pass
    ... else: assert 0, 'FAILED'
    """

def test_reduce():
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(test_reduce))()
    'Hello, world!'
    """
    return 'Hello, world!'

def test_method(self):
    return self

class BindingTest:
    """
    >>> BindingTest.test_method = test_method
    >>> BindingTest.test_method() #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> BindingTest().test_method()
    <BindingTest instance>
    """
    def __repr__(self):
        return '<BindingTest instance>'


def codeof(func):
    if IS_PY3:
        return func.__code__
    else:
        return func.func_code

def varnamesof(func):
    code = codeof(func)
    varnames = code.co_varnames
    if sys.version_info < (2,5):
        pos = {'a':0, 'x':1, 'b':2, 'l':3, 'm':4}
        varnames = tuple(sorted(varnames, key=pos.__getitem__))
    return varnames

def namesof(func):
    code = codeof(func)
    names = code.co_names
    if sys.version_info < (2,5):
        names = ()
    return names

def cy_no_arg():
    l = m = 1
def cy_one_arg(a):
    l = m = 1
def cy_two_args(x, b):
    l = m = 1
def cy_default_args(x=1, b=2):
    l = m = 1

def test_code():
    """
    >>> def no_arg(): l = m = 1
    >>> def one_arg(a): l = m = 1
    >>> def two_args(x, b): l = m = 1
    >>> def default_args(x=1, b=2): l = m = 1

    >>> codeof(no_arg).co_argcount
    0
    >>> codeof(cy_no_arg).co_argcount
    0
    >>> print(codeof(no_arg).co_name)
    no_arg
    >>> print(codeof(cy_no_arg).co_name)
    cy_no_arg
    >>> namesof(no_arg)
    ()
    >>> codeof(cy_no_arg).co_names
    ()
    >>> varnamesof(no_arg)
    ('l', 'm')
    >>> codeof(cy_no_arg).co_varnames
    ('l', 'm')

    >>> codeof(one_arg).co_argcount
    1
    >>> codeof(cy_one_arg).co_argcount
    1
    >>> print(codeof(one_arg).co_name)
    one_arg
    >>> print(codeof(cy_one_arg).co_name)
    cy_one_arg
    >>> namesof(one_arg)
    ()
    >>> codeof(cy_one_arg).co_names
    ()
    >>> varnamesof(one_arg)
    ('a', 'l', 'm')
    >>> codeof(cy_one_arg).co_varnames
    ('a', 'l', 'm')

    >>> codeof(two_args).co_argcount
    2
    >>> codeof(cy_two_args).co_argcount
    2
    >>> namesof(two_args)
    ()
    >>> codeof(cy_two_args).co_names
    ()
    >>> varnamesof(two_args)
    ('x', 'b', 'l', 'm')
    >>> codeof(cy_two_args).co_varnames
    ('x', 'b', 'l', 'm')

    >>> codeof(default_args).co_argcount
    2
    >>> codeof(cy_default_args).co_argcount
    2
    >>> namesof(default_args)
    ()
    >>> codeof(cy_default_args).co_names
    ()
    >>> varnamesof(default_args)
    ('x', 'b', 'l', 'm')
    >>> codeof(cy_default_args).co_varnames
    ('x', 'b', 'l', 'm')
    """


def test_annotations(a: "test", b: "other" = 2, c: 123 = 4) -> "ret":
    """
    >>> isinstance(test_annotations.__annotations__, dict)
    True
    >>> sorted(test_annotations.__annotations__.items())
    [('a', 'test'), ('b', 'other'), ('c', 123), ('return', 'ret')]

    >>> def func_b(): return 42
    >>> def func_c(): return 99
    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 99), ('x', 'banana'), ('y', 42)]

    >>> inner.__annotations__ = {234: 567}
    >>> inner.__annotations__
    {234: 567}
    >>> inner.__annotations__ = None
    >>> inner.__annotations__
    {}
    >>> inner.__annotations__ = 321
    Traceback (most recent call last):
    TypeError: __annotations__ must be set to a dict object
    >>> inner.__annotations__
    {}

    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 99), ('x', 'banana'), ('y', 42)]
    >>> inner.__annotations__['abc'] = 66
    >>> sorted(inner.__annotations__.items())
    [('abc', 66), ('return', 99), ('x', 'banana'), ('y', 42)]

    >>> inner = test_annotations(1, func_b, func_c)
    >>> sorted(inner.__annotations__.items())
    [('return', 99), ('x', 'banana'), ('y', 42)]
    """
    def inner(x: "banana", y: b()) -> c():
        return x,y
    return inner


def add_one(func):
    "Decorator to add 1 to the last argument of the function call"
    def inner(*args):
        args = args[:-1] + (args[-1] + 1,)
        return func(*args)
    return inner

@add_one
def test_decorated(x):
    """
    >>> test_decorated(0)
    1
    """
    return x

@add_one
@add_one
def test_decorated2(x):
    """
    >>> test_decorated2(0)
    2
    """
    return x


cdef class TestDecoratedMethods:
    @add_one
    def test(self, x):
        """
        >>> TestDecoratedMethods().test(0)
        1
        """
        return x

    @add_one
    @add_one
    def test2(self, x):
        """
        >>> TestDecoratedMethods().test2(0)
        2
        """
        return x

    def test_calls(self, x):
        """
        >>> TestDecoratedMethods().test_calls(2)
        25
        """
        return self.test(x) + self.test2(x*10)


cdef class TestUnboundMethodCdef:
    """
    >>> C = TestUnboundMethodCdef
    >>> IS_PY2 or (C.meth is C.__dict__["meth"])
    True
    """
    def meth(self): pass


class TestUnboundMethod:
    """
    >>> C = TestUnboundMethod
    >>> IS_PY2 or (C.meth is C.__dict__["meth"])
    True
    """
    def meth(self): pass


cdef class TestOptimisedBuiltinMethod:
    """
    >>> obj = TestOptimisedBuiltinMethod()
    >>> obj.append(2)
    3
    >>> obj.call(2)
    4
    >>> obj.call(3, obj)
    5
    """
    def append(self, arg):
        print(arg+1)

    def call(self, arg, obj=None):
        (obj or self).append(arg+1)  # optimistically optimised => uses fast fallback method call
