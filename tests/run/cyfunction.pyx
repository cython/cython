# cython: binding=True
# mode: run
# tag: cyfunction

import sys
IS_PY3 = sys.version_info[0] >= 3

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


def test_qualname():
    """
    >>> test_qualname.__qualname__
    'test_qualname'
    >>> test_qualname.__qualname__ = 123 #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: __qualname__ must be set to a ... object
    >>> test_qualname.__qualname__ = 'foo'
    >>> test_qualname.__qualname__
    'foo'
    """


def test_nested_qualname():
    """
    >>> func, lambda_func = test_nested_qualname()

    >>> func().__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test'
    >>> func().test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'
    >>> func()().test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'

    >>> lambda_func.__qualname__
    'test_nested_qualname.<locals>.<lambda>'
    """
    def outer():
        class Test(object):
            def test(self):
                return 123
        return Test
    return outer, lambda:None


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
