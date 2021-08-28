# mode: run

# https://github.com/cython/cython/issues/4350
# In some circumstances it's possible to multiply inherit Python classes
# from cdef classes in ways that cause __cinit__ and __dealloc__ not to
# be called.

# The tests work on Python<3.6 because Cython itself calls __init_subclass__.
# If they were written using exec then they would be fail there.

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

def test_BaseC_A():
    """
    >>> test_BaseC_A()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Invalid inheritance from cdef class A: ...
    """
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
    """
    >>> test_X_Y() # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Invalid inheritance from cdef class Y: ...
    """
    class C(X, Y):
        pass

    C()

def test_Y_X():
    """
    >>> test_Y_X()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Invalid inheritance from cdef class X: ...
    """
    class C(Y, X):
        pass

    C()
