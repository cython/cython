# mode: run
# ticket: t295

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


def func0():
    """
    >>> func0()
    >>> func0(**{})
    """

def func1(arg):
    """
    >>> func1(None)
    >>> func1(*[None])
    >>> func1(arg=None)
    """
    return arg

def func1_unused(arg):
    """
    >>> func1_unused(None)
    >>> func1_unused(*[None])
    >>> func1_unused(arg=None)
    """

@cython.always_allow_keywords(False)
def func2(arg):
    """
    >>> func2(None)
    >>> func2(*[None])
    >>> assert_typeerror_no_keywords(func2, arg=None)
    """
    return arg

@cython.always_allow_keywords(False)
def func2_unused(arg):
    """
    >>> func2_unused(None)
    >>> func2_unused(*[None])
    >>> assert_typeerror_no_keywords(func2_unused, arg=None)
    """

@cython.always_allow_keywords(True)
def func3(arg):
    """
    >>> func3(None)
    >>> func3(*[None])
    >>> func3(arg=None)
    """
    return arg

@cython.always_allow_keywords(True)
def func3_unused(arg):
    """
    >>> func3_unused(None)
    >>> func3_unused(*[None])
    >>> func3_unused(arg=None)
    """

cdef class A:
    """
    >>> class PyA(object):
    ...     def meth0(self): pass
    ...     def meth1(self, arg): pass

    >>> PyA().meth0()
    >>> PyA.meth0(PyA())
    >>> PyA.meth0(self=PyA())
    >>> try: PyA().meth0(self=PyA())
    ... except TypeError as exc: assert 'multiple' in str(exc), "Unexpected message: %s" % exc
    ... else: assert False, "No TypeError when passing 'self' argument twice"

    >>> PyA().meth1(1)
    >>> PyA.meth1(PyA(), 1)
    >>> PyA.meth1(PyA(), arg=1)
    >>> PyA.meth1(self=PyA(), arg=1)
    """

    @cython.always_allow_keywords(False)
    def meth0_nokw(self):
        """
        >>> A().meth0_nokw()
        >>> A().meth0_nokw(**{})
        >>> try: pass  #A.meth0_nokw(self=A())
        ... except TypeError as exc: assert 'needs an argument' in str(exc), "Unexpected message: %s" % exc
        ... else: pass  #assert False, "No TypeError for missing 'self' positional argument"
        """

    @cython.always_allow_keywords(True)
    def meth0_kw(self):
        """
        >>> A().meth0_kw()
        >>> A().meth0_kw(**{})
        >>> A.meth0_kw(A())
        >>> #A.meth0_kw(self=A())
        >>> try: pass  #A().meth0_kw(self=A())
        ... except TypeError as exc: assert 'multiple' in str(exc), "Unexpected message: %s" % exc
        ... else: pass  #assert False, "No TypeError when passing 'self' argument twice"
        """

    @cython.always_allow_keywords(True)
    def meth1_kw(self, arg):
        """
        >>> A().meth1_kw(None)
        >>> A().meth1_kw(*[None])
        >>> A().meth1_kw(arg=None)
        >>> A.meth1_kw(A(), arg=None)
        >>> #A.meth1_kw(self=A(), arg=None)
        """

    @cython.always_allow_keywords(False)
    def meth1_nokw(self, arg):
        """
        >>> A().meth1_nokw(None)
        >>> A().meth1_nokw(*[None])
        >>> assert_typeerror_no_keywords(A().meth1_nokw, arg=None)
        >>> assert_typeerror_no_keywords(A.meth1_nokw, A(), arg=None)
        >>> try: pass  # A.meth1_nokw(self=A(), arg=None)
        ... except TypeError as exc: assert 'needs an argument' in str(exc), "Unexpected message: %s" % exc
        ... else: pass  # assert False, "No TypeError for missing 'self' positional argument"
        """

    @cython.always_allow_keywords(False)
    def meth2(self, arg):
        """
        >>> A().meth2(None)
        >>> A().meth2(*[None])
        >>> assert_typeerror_no_keywords(A().meth2, arg=None)
        """

    @cython.always_allow_keywords(True)
    def meth3(self, arg):
        """
        >>> A().meth3(None)
        >>> A().meth3(*[None])
        >>> A().meth3(arg=None)
        """


class B(object):
    @cython.always_allow_keywords(False)
    def meth0_nokw(self):
        """
        >>> B().meth0_nokw()
        >>> B().meth0_nokw(**{})
        >>> assert_typeerror_no_keywords(B.meth0_nokw, self=B())
        """

    @cython.always_allow_keywords(True)
    def meth0_kw(self):
        """
        >>> B().meth0_kw()
        >>> B().meth0_kw(**{})
        >>> B.meth0_kw(B())
        >>> B.meth0_kw(self=B())
        >>> try: B().meth0_kw(self=B())
        ... except TypeError as exc: assert 'multiple' in str(exc), "Unexpected message: %s" % exc
        ... else: assert False, "No TypeError when passing 'self' argument twice"
        """

    @cython.always_allow_keywords(True)
    def meth1(self, arg):
        """
        >>> B().meth1(None)
        >>> B().meth1(*[None])
        >>> B().meth1(arg=None)
        >>> B.meth1(B(), arg=None)
        >>> B.meth1(self=B(), arg=None)
        """

    @cython.always_allow_keywords(False)
    def meth2(self, arg):
        """
        >>> B().meth2(None)
        >>> B().meth2(*[None])
        >>> B.meth2(B(), None)
        >>> B.meth2(self=B(), arg=None)
        >>> B().meth2(arg=None)  # assert_typeerror_no_keywords(B().meth2, arg=None)  -> not a cdef class!
        """

    @cython.always_allow_keywords(True)
    def meth3(self, arg):
        """
        >>> B().meth3(None)
        >>> B().meth3(*[None])
        >>> B().meth3(arg=None)
        """
