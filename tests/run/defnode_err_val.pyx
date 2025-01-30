# mode: run

cdef class TestErrVal(object):
    def __cinit__(self, TestErrVal a):
        pass


def test_errval():
    """
    >>> test_errval() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Argument 'a' has incorrect type (expected...TestErrVal, got int)
    """
    TestErrVal(123)
