from cython cimport typeof

ctypedef bint mybool

cdef mybool mybul = True
cdef bint bul = True
cdef int num = 42


def CondExprNode_to_obj(test):
    """
    >>> CondExprNode_to_obj(True)
    True
    2
    >>> CondExprNode_to_obj(False)
    True
    84
    """

    print(typeof(mybul if test else num) == typeof(bul if test else num) == typeof(object))

    return (mybul if test else num) + (bul if test else num)


def BoolBinopNode_to_obj():
    """
    >>> BoolBinopNode_to_obj()
    True
    2
    """

    print(typeof(mybul or num) == typeof(bul or num) == typeof(object))

    return (mybul or num) + (bul or num)


cdef int test_bool(mybool arg):
    return <int>arg


def CondExprNode_to_bool(test):
    """
    >>> CondExprNode_to_bool(True)
    True
    0
    >>> CondExprNode_to_bool(False)
    True
    2
    """

    print(typeof(not mybul if test else mybul) == typeof(not bul if test else bul) == typeof(bul))

    # test_bool would silently crash if one of the types is casted
    # to Python object and not just assigned.
    # It happens when type is wrongly inferred to Python object
    # and not bin or mybool.
    return test_bool(not mybul if test else mybul) + test_bool(not bul if test else bul)


def BoolBinopNode_to_bool():
    """
    >>> BoolBinopNode_to_bool()
    True
    2
    """

    print(typeof(not mybul or mybul) == typeof(not bul or bul) == typeof(bul))

    return test_bool(not mybul or mybul) + test_bool(not bul or bul)
