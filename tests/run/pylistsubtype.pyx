__doc__ = u"""
    >>> l1 = Sub1([1,2,3])
    >>> len(l1)
    3

    >>> l2 = Sub2([1,2,3])
    >>> len(l2)
    3

    >>> isinstance(l1, list)
    True
    >>> isinstance(l2, list)
    True
    >>> isinstance(l1, Sub1)
    True
    >>> isinstance(l1, Sub2)
    True
    >>> isinstance(l2, Sub1)
    False
    >>> isinstance(l2, Sub2)
    True
"""

cdef extern from *:
    ctypedef class __builtin__.list [ object PyListObject ]:
        pass

cdef class Sub2(list):
    cdef char character

cdef class Sub1(Sub2):
    pass
