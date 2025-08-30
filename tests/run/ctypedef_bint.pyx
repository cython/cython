from __future__ import print_function

from cython cimport typeof

ctypedef bint mybool

cdef mybool mybul = True
cdef bint bul = True
cdef int num = 42


def CondExprNode_to_obj(test):
    """
    >>> CondExprNode_to_obj(True)
    Python object | Python object
    2
    >>> CondExprNode_to_obj(False)
    Python object | Python object
    84
    """

    print(typeof(mybul if test else num), "|", typeof(bul if test else num))

    return (mybul if test else num) + (bul if test else num)


def BoolBinopNode_to_obj():
    """
    >>> BoolBinopNode_to_obj()
    Python object | Python object
    2
    """

    print(typeof(mybul or num), "|", typeof(bul or num))

    return (mybul or num) + (bul or num)


cdef int test_bool(mybool arg):
    return <int>arg


def CondExprNode_to_bool(test):
    """
    >>> CondExprNode_to_bool(True)
    bint | bint
    0
    >>> CondExprNode_to_bool(False)
    bint | bint
    2
    """

    print(typeof(not mybul if test else mybul), "|", typeof(not bul if test else bul))

    # test_bool() would silently crash if one of the types is cast
    # to Python object and not just assigned.
    # It happens when a type is wrongly inferred as Python object
    # instead of bint or mybool.
    return test_bool(not mybul if test else mybul) + test_bool(not bul if test else bul)


def BoolBinopNode_to_bool():
    """
    >>> BoolBinopNode_to_bool()
    bint | bint
    2
    """

    print(typeof(not mybul or mybul), "|", typeof(not bul or bul))

    return test_bool(not mybul or mybul) + test_bool(not bul or bul)
