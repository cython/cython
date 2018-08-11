# ticket: 601

cdef unsigned long size2():
    return 3

def for_from_plain_ulong():
    """
    >>> for_from_plain_ulong()
    0
    1
    2
    """
    cdef object j = 0
    for j from 0 <= j < size2():
        print j

def for_in_plain_ulong():
    """
    >>> for_in_plain_ulong()
    0
    1
    2
    """
    cdef object j = 0
    for j in range(size2()):
        print j


cdef extern from *:
    """typedef unsigned long Ulong;"""
    ctypedef unsigned long Ulong

cdef Ulong size():
    return 3

def for_from_ctypedef_ulong():
    """
    >>> for_from_ctypedef_ulong()
    0
    1
    2
    """
    cdef object j = 0
    for j from 0 <= j < size():
        print j

def for_in_ctypedef_ulong():
    """
    >>> for_in_ctypedef_ulong()
    0
    1
    2
    """
    cdef object j = 0
    for j in range(size()):
        print j


class ForFromLoopInPyClass(object):
    """
    >>> ForFromLoopInPyClass.i    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...ForLoopInPyClass... has no attribute ...i...
    >>> ForFromLoopInPyClass.k
    0
    >>> ForFromLoopInPyClass.m
    1
    """
    for i from 0 <= i < 1:
        pass

    for k from 0 <= k < 2:
        pass

    for m from 0 <= m < 3:
        pass
