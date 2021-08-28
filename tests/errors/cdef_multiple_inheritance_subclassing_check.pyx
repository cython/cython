# mode: run

# https://github.com/cython/cython/issues/4350
# In some circumstances it's possible to multiply inherit Python classes
# from cdef classes in ways that cause __cinit__ and __dealloc__ not to
# be called.
# On Python 3.6+ it's possible to validate this
import sys

cdef class BaseA:
    cdef int x

    def __cinit__(self):
        print "BaseA.__cinit__"

cdef class A(BaseA):
    # layout compatible with (and derived from) A
    def __cinit__(self):
        print "A.__cinit__"

cdef class X:
    def __cinit__(self):
        print "X.__cinit__"

cdef class Y:
    # layout compatible with X
    def __cinit__(self):
        print "Y.__cinit__"

class BaseC(BaseA):
        pass


if sys.version_info >= (3, 6):
    __doc__ = """
        >>> test_BaseC_A()  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Invalid inheritance from cdef class A: ...

        >>> test_X_Y() # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Invalid inheritance from cdef class Y: ...

        >>> test_Y_X() # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Invalid inheritance from cdef class X: ...
    """


def test_BaseC_A():
    # will fail with an exception - test in module __doc__
    class C(BaseC, A):
        pass

    C()

def test_A_BaseC():
    """
    Should work so we just test the constructors are right
    >>> test_A_BaseC()
    BaseA.__cinit__
    A.__cinit__
    """
    class C(A, BaseC):
        pass

    C()

def test_X_Y():
    # will fail with an exception - test in module __doc__
    class C(X, Y):
        pass

    C()

def test_Y_X():
    # will fail with an exception - test in module __doc__
    class C(Y, X):
        pass

    C()
