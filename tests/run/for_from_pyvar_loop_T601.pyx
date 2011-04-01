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


cdef extern from "for_from_pyvar_loop_T601_extern_def.h":
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
