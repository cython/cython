# ticket: t417
#cython: autotestdict=True

cdef class Foo:
    cdef int i
    def __cinit__(self):
        self.i = 1

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

def attribute_access(arg):
    """
    >>> attribute_access(Foo())
    >>> attribute_access(SubFoo())
    >>> attribute_access(None)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert NoneType to typetest_T417.Foo
    >>> attribute_access(123)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert int to typetest_T417.Foo
    >>> attribute_access(Bar())
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert typetest_T417.Bar to typetest_T417.Foo
    """
    cdef val = (<Foo?>arg).i


cdef int count = 0

cdef object getFoo():
     global count
     count += 1
     return Foo()

def test_getFoo():
    """
    >>> test_getFoo()
    1
    """
    cdef int old_count = count
    cdef Foo x = getFoo()
    return count - old_count

def test_getFooCast():
    """
    >>> test_getFooCast()
    1
    """
    cdef int old_count = count
    cdef Foo x = <Foo?>getFoo()
    return count - old_count

def test_builtin_typecheck_cast(maybe_list):
    """
    >>> test_builtin_typecheck_cast([])
    []
    >>> test_builtin_typecheck_cast({})
    Traceback (most recent call last):
       ...
    TypeError: Expected list, got dict
    """
    return <list?>maybe_list
