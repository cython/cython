__doc__ = u"""
__getattribute__ and __getattr__ special methods and subclasses.

getattr does not override members.
    >>> a = getattr_boring()
    >>> a.boring_member
    10
    >>> print(a.resolved_by)
    getattr_boring

getattribute does.
    >>> a = getattribute_boring()
    >>> a.boring_member
    Traceback (most recent call last):
    AttributeError
    >>> print(a.resolved_by)
    getattribute_boring

Is inherited.
    >>> a = boring_boring_getattribute()
    >>> a.boring_getattribute_member
    Traceback (most recent call last):
    AttributeError
    >>> a.boring_boring_getattribute_member
    Traceback (most recent call last):
    AttributeError
    >>> print(a.resolved_by)
    _getattribute

__getattribute__ is always tried first, then __getattr__, regardless of where
in the inheritance hiarchy they came from.
    >>> a = getattribute_boring_boring_getattr()
    >>> a.foo
    Traceback (most recent call last):
    AttributeError
    >>> print(a.resolved_by)
    getattribute_boring_boring_getattr
    >>> a.getattribute_boring_boring_getattr
    True
    >>> a._getattr
    True

    >>> a = getattr_boring_boring_getattribute()
    >>> a.foo
    Traceback (most recent call last):
    AttributeError
    >>> print(a.resolved_by)
    _getattribute
    >>> a.getattr_boring_boring_getattribute
    True
    >>> a._getattribute
    True

"""

cdef class boring:
    cdef readonly int boring_member
    def __init__(self):
        self.boring_member = 10

cdef class getattr_boring(boring):
    def __getattr__(self,n):
        if n == u'resolved_by':
            return u'getattr_boring'
        elif n == u'getattr_boring':
            return True
        else:
            raise AttributeError

cdef class getattribute_boring(boring):
    def __getattribute__(self,n):
        if n == u'resolved_by':
            return u'getattribute_boring'
        elif n == u'getattribute_boring':
            return True
        else:
            raise AttributeError

cdef class _getattr:
    def __getattr__(self,n):
        if n == u'resolved_by':
            return u'_getattr'
        elif n == u'_getattr':
            return True
        else:
            raise AttributeError

cdef class _getattribute(boring):
    def __getattribute__(self,n):
        if n == u'resolved_by':
            return u'_getattribute'
        elif n == u'_getattribute':
            return True
        else:
            raise AttributeError

cdef class boring_getattribute(_getattribute):
    cdef readonly int boring_getattribute_member

cdef class boring_boring_getattribute(boring_getattribute):
    cdef readonly int boring_boring_getattribute_member

cdef class boring_getattr(_getattr):
    cdef readonly int boring_getattr_member

cdef class boring_boring_getattr(boring_getattr):
    cdef readonly int boring_boring_getattr_member

cdef class getattribute_boring_boring_getattr(boring_boring_getattr):
    def __getattribute__(self,n):
        if n == u'resolved_by':
            return u'getattribute_boring_boring_getattr'
        elif n == u'getattribute_boring_boring_getattr':
            return True
        else:
            raise AttributeError

cdef class getattr_boring_boring_getattribute(boring_boring_getattribute):
    def __getattr__(self,n):
        if n == u'resolved_by':
            return u'getattr_boring_boring_getattribute'
        elif n == u'getattr_boring_boring_getattribute':
            return True
        else:
            raise AttributeError
