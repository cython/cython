# ticket: 608

cdef class MyInt(int):
    """
    >>> MyInt(2) == 2
    True
    >>> MyInt(2).attr is None
    True
    """
    cdef readonly object attr

cdef class MyInt2(int):
    """
    >>> MyInt2(2) == 2
    True
    >>> MyInt2(2).attr is None
    True
    >>> MyInt2(2).test(3)
    5
    """
    cdef readonly object attr

    def test(self, arg):
        return self._test(arg)

    cdef _test(self, arg):
        return self + arg

cdef class MyInt3(MyInt2):
    """
    >>> MyInt3(2) == 2
    True
    >>> MyInt3(2).attr is None
    True
    >>> MyInt3(2).test(3)
    6
    """
    cdef _test(self, arg):
        return self + arg + 1

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
    >>> MyUnicode(ustring + ustring) == ustring
    False
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

cdef class MyListOverride(list):
    """
    >>> MyListOverride([1,2,3]) == [1,2,3]
    True
    >>> l = MyListOverride([1,2,3])
    >>> l.reverse()
    >>> l
    [1, 2, 3, 5]
    >>> l._reverse()
    >>> l
    [1, 2, 3, 5, 5]
    """
    # not doctested:
    """
    >>> l = MyListOverride([1,2,3])
    >>> l.append(8)
    >>> l
    [1, 2, 3, 0, 8]
    >>> l._append(9)
    >>> l
    [1, 2, 3, 0, 8, 0, 9]
    """
    def reverse(self):
        self[:] = self + [5]

    def _reverse(self):
        self.reverse()

    ## FIXME: this doesn't currently work:

    ## cdef int append(self, value) except -1:
    ##     self[:] = self + [0] + [value]
    ##     return 0

    ## def _append(self, value):
    ##     self.append(value)

cdef class MyDict(dict):
    """
    >>> MyDict({1:2, 3:4}) == {1:2, 3:4}
    True
    >>> MyDict({1:2, 3:4}).attr is None
    True
    """
    cdef readonly object attr
