# ticket: 295

cimport cython

def assert_typeerror_no_keywords(func, *args, **kwds):
    # Python 3.9 produces an slightly different error message
    # to previous versions, so doctest isn't matching the
    # traceback
    try:
        func(*args, **kwds)
    except TypeError as e:
        assert e.args[0].endswith(" takes no keyword arguments"), e.args[0]
    else:
        assert False, "call did not raise TypeError"


def func1(arg):
    """
    >>> func1(None)
    >>> func1(*[None])
    >>> assert_typeerror_no_keywords(func1, arg=None)
    """
    pass

@cython.always_allow_keywords(False)
def func2(arg):
    """
    >>> func2(None)
    >>> func2(*[None])
    >>> assert_typeerror_no_keywords(func2, arg=None)
    """
    pass

@cython.always_allow_keywords(True)
def func3(arg):
    """
    >>> func3(None)
    >>> func3(*[None])
    >>> func3(arg=None)
    """
    pass

cdef class A:
    """
    >>> A().meth1(None)
    >>> A().meth1(*[None])
    >>> assert_typeerror_no_keywords(A().meth1, arg=None)
    >>> A().meth2(None)
    >>> A().meth2(*[None])
    >>> assert_typeerror_no_keywords(A().meth2, arg=None)
    >>> A().meth3(None)
    >>> A().meth3(*[None])
    >>> A().meth3(arg=None)
    """

    def meth1(self, arg):
        pass

    @cython.always_allow_keywords(False)
    def meth2(self, arg):
        pass

    @cython.always_allow_keywords(True)
    def meth3(self, arg):
        pass
