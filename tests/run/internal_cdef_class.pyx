
cimport cython


@cython.internal
cdef class InternalType:
    """
    NOTE: this doesn't fail because it is never tested !
    >>> i = InternalType
    """

cdef class PublicType:
    """
    >>> p = PublicType
    """

def test():
    """
    >>> p,i = test()

    >>> p = PublicType

    >>> i = InternalType         # doctest: +ELLIPSIS
    Traceback (most recent call last):
    NameError: ...name 'InternalType' is not defined
    """
    p = PublicType
    i = InternalType
    return p,i
