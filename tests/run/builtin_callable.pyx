# mode: run
# tag: builtin, callable

cimport cython

@cython.test_assert_path_exists("//SimpleCallNode[@type.is_pyobject = False]")
def test_callable(x):
    """
    >>> test_callable(None)
    False
    >>> test_callable('ABC')
    False

    >>> class C: pass
    >>> test_callable(C)
    True
    >>> test_callable(C())
    False

    >>> class M(type): pass
    >>> class X(metaclass=M): pass
    >>> callable(X)
    True
    >>> test_callable(X)
    True

    >>> test_callable(int)
    True
    >>> test_callable(test_callable)
    True
    """
    b = callable(x)
    return b
