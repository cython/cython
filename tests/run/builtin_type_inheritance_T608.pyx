
cdef class MyInt(int):
    """
    >>> MyInt(2) == 2
    True
    >>> MyInt(2).attr is None
    True
    """
    cdef readonly object attr

cdef class MyFloat(float):
    """
    >>> MyFloat(1.0)== 1.0
    True
    >>> MyFloat(1.0).attr is None
    True
    """
    cdef readonly object attr

ustring = u'abc'

cdef class MyUnicode(unicode):
    """
    >>> MyUnicode(ustring) == ustring
    True
    >>> MyUnicode(ustring).attr is None
    True
    """
    cdef readonly object attr

cdef class MyList(list):
    """
    >>> MyList([1,2,3]) == [1,2,3]
    True
    >>> MyList([1,2,3]).attr is None
    True
    """
    cdef readonly object attr

cdef class MyDict(dict):
    """
    >>> MyDict({1:2, 3:4}) == {1:2, 3:4}
    True
    >>> MyDict({1:2, 3:4}).attr is None
    True
    """
    cdef readonly object attr
