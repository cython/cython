#cython: autotestdict=True

cdef class Foo:
    pass

cdef class SubFoo(Foo):
    pass

cdef class Bar:
    pass

def foo1(arg):
    """
    >>> foo1(Foo())
    >>> foo1(SubFoo())
    >>> foo1(None)
    >>> foo1(123)
    >>> foo1(Bar())
    """
    cdef Foo val = <Foo>arg

def foo2(arg):
    """
    >>> foo2(Foo())
    >>> foo2(SubFoo())
    >>> foo2(None)
    >>> foo2(123)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert int to typetest_T417.Foo
    >>> foo2(Bar())
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert typetest_T417.Bar to typetest_T417.Foo
    """
    cdef Foo val = arg

def foo3(arg):
    """
    >>> foo3(Foo())
    >>> foo3(SubFoo())
    >>> foo3(None)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert NoneType to typetest_T417.Foo
    >>> foo3(123)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert int to typetest_T417.Foo
    >>> foo2(Bar())
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert typetest_T417.Bar to typetest_T417.Foo
    """
    cdef val = <Foo?>arg
