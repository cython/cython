
cimport cython

@cython.final
cdef class FinalClass:
    """
    >>> f = FinalClass()
    >>> test_final_class(f)
    Type tested

    >>> try:
    ...     class SubType(FinalClass): pass
    ... except TypeError:
    ...     print('PASSED!')
    PASSED!
    """

cdef class NonFinalClass:
    """
    >>> class SubType(NonFinalClass): pass
    >>> s = SubType()
    """

@cython.final
cdef class FinalSubClass(NonFinalClass):
    """
    >>> f = FinalSubClass()
    >>> test_non_final_class(f)
    Type tested

    >>> try:
    ...     class SubType(FinalSubClass): pass
    ... except TypeError:
    ...     print('PASSED!')
    PASSED!
    """


def test_final_class(FinalClass c):
    print u"Type tested"

def test_non_final_class(NonFinalClass c):
    print u"Type tested"
