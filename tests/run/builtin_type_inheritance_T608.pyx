# ticket: t608

# see "builtin_type_inheritance_T608_py2only.pyx" for inheritance from int

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

cdef class MyException(Exception):
    """
    >>> raise MyException(3) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    MyException: 3
    """
    cdef readonly int value
    def __cinit__(self, value):
        self.value = value

def test_exception_isinstance(maybe_exn):
    """
    >>> test_exception_isinstance(Exception())
    True
    >>> test_exception_isinstance(MyException(3))
    True
    >>> test_exception_isinstance(3)
    False
    """
    return isinstance(maybe_exn, Exception)

def test_exception_type_cast(Exception maybe_exn):
    """
    >>> test_exception_type_cast(Exception())
    >>> test_exception_type_cast(MyException(3))
    >>> test_exception_type_cast(3)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Argument 'maybe_exn' has incorrect type (expected ...Exception, got int)
    """
    cdef object o = maybe_exn
    cdef Exception e = o
