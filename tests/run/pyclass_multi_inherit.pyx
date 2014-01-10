# mode: run

"""
http://thread.gmane.org/gmane.comp.python.cython.user/10267

The problem here was that CPython complained about calls to a type's
__new__() being unsafe when it has a different tp_new() than object
but the same memory layout.
"""


cdef class A(object):
    # larger than object
    cdef int a

cdef class B(object):
    # same memory layout as object
    pass

cinit_called = []

cdef class Cinit(object):
    # same memory layout as object but with __cinit__
    def __cinit__(self):
        cinit_called.append(self)


class C(object):
    """
    >>> o = C.__new__(C)
    """

# subtypes of B

class CB(C,B):
    """
    >>> o = CB.__new__(CB)
    """

class BC(B,C):
    """
    >>> o = BC.__new__(BC)
    """

# subtypes of A

class CA(C,A):
    """
    >>> o = CA.__new__(CA)
    """

class AC(A,C):
    """
    >>> o = AC.__new__(AC)
    """

# subtypes of Cinit

class CCinit(C, Cinit):
    """
    >>> o = CCinit.__new__(CCinit)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...is not safe...
    >>> del cinit_called[:]
    """

class CinitC(Cinit, C):
    """
    >>> o = CinitC.__new__(CinitC)
    >>> o in cinit_called
    True
    >>> del cinit_called[:]
    """
