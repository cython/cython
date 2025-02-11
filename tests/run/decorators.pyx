__doc__ = u"""
  >>> f(1,2)
  4
  >>> f.HERE
  1

  >>> g(1,2)
  5
  >>> g.HERE
  5

  >>> h(1,2)
  6
  >>> h.HERE
  1
  >>> i(4)
  3
  >>> i.HERE
  1
  >>> i_called_directly(4)
  3
  >>> i_called_directly.HERE
  1
"""

class wrap:
    def __init__(self, func):
        self.func = func
        self.HERE = 1
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def decorate(func):
    try:
        func.HERE += 1
    except AttributeError:
        func = wrap(func)
    return func

def decorate2(a,b):
    return decorate

@decorate
def f(a,b):
    return a+b+1

@decorate
@decorate
@decorate
@decorate
@decorate
def g(a,b):
    return a+b+2

@decorate2(1,2)
def h(a,b):
    return a+b+3

class A:
    def decorate(self, func):
        return decorate(func)


a = A()
@a.decorate
def i(x):
    return x - 1

@A().decorate
def i_called_directly(x):
    # PEP 614 means this now works
    return x - 1

list_of_decorators = [decorate, decorate2]

@list_of_decorators[0]
def test_index_from_decorator_list0(a, b):
    """
    PEP 614 means this now works
    >>> test_index_from_decorator_list0(1, 2)
    4
    >>> test_index_from_decorator_list0.HERE
    1
    """
    return a+b+1

@list_of_decorators[1](1,2)
def test_index_from_decorator_list1(a, b):
    """
    PEP 614 means this now works
    >>> test_index_from_decorator_list1(1, 2)
    4
    >>> test_index_from_decorator_list1.HERE
    1
    """
    return a+b+1

def append_to_list_decorator(lst):
    def do_append_to_list_dec(func):
        def new_func():
            return lst + func()
        return new_func
    return do_append_to_list_dec

def outer(arg1, arg2):
    """
    ensure decorators are analysed in the correct scope
    https://github.com/cython/cython/issues/4367
    mainly intended as a compile-time test (but it does run...)
    >>> outer(append_to_list_decorator, [1,2,3])
    [1, 2, 3, 4]
    """
    @arg1([x for x in arg2])
    def method():
        return [4]
    return method()

class HasProperty(object):
    """
    >>> hp = HasProperty()
    >>> hp.value
    0
    >>> hp.value = 1
    >>> hp.value
    1
    """
    def __init__(self) -> None:
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    # https://github.com/cython/cython/issues/4836
    # The variable tracker was confusing "value" in the decorator
    # for "value" in the argument list
    @value.setter
    def value(self, value: int):
        self._value = value
