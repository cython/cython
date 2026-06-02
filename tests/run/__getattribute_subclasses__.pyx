# mode: run

# __getattribute__ and __getattr__ special methods and subclasses.

cdef class boring:
    cdef readonly int boring_member
    cdef readonly int getattr_called
    cdef int getattribute_called
    def __init__(self):
        self.boring_member = 10

cdef class getattr_boring(boring):
    """
    getattr does not override members.

    >>> a = getattr_boring()
    >>> a.boring_member
    10
    >>> a.getattr_called
    0
    >>> print(a.resolved_by)
    getattr_boring
    >>> a.getattr_called
    1
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattr_called
    2
    """
    def __getattr__(self,n):
        self.getattr_called += 1
        if n == 'resolved_by':
            return 'getattr_boring'
        elif n == 'getattr_boring':
            return True
        else:
            raise AttributeError


# currently fails, see #1793
#class getattr_boring_py(getattr_boring):
#    __doc__ = getattr_boring.__doc__.replace(
#        'getattr_boring()', 'getattr_boring_py()')


cdef class getattribute_boring(boring):
    """
    getattribute overrides members.

    >>> a = getattribute_boring()
    >>> a.getattribute_called
    1
    >>> try: a.boring_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    3
    >>> print(a.resolved_by)
    getattribute_boring
    >>> a.getattribute_called
    5
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    7
    """
    def __getattribute__(self,n):
        self.getattribute_called += 1
        if n == 'resolved_by':
            return 'getattribute_boring'
        elif n == 'getattribute_boring':
            return True
        elif n == 'getattribute_called':
            return self.getattribute_called
        else:
            raise AttributeError


class getattribute_boring_py(getattribute_boring):
    __doc__ = getattribute_boring.__doc__.replace(
        'getattribute_boring()', 'getattribute_boring_py()')


cdef class _getattr:
    cdef readonly int getattr_called
    def __getattr__(self,n):
        self.getattr_called += 1
        if n == 'resolved_by':
            return '_getattr'
        elif n == '_getattr':
            return True
        elif n == 'getattr_called':
            # must only get here if __getattribute__ is overwritten
            assert 'getattribute' in type(self).__name__
            return self.getattr_called
        else:
            raise AttributeError


class getattr_py(_getattr):
    """
    getattr is inherited.

    >>> a = getattr_py()
    >>> a.getattr_called
    0
    >>> print(a.resolved_by)
    _getattr
    >>> a.getattr_called
    1
    >>> print(a._getattr)
    True
    >>> a.getattr_called
    2
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")

    # currently fails, see #1793
    #>>> a.getattr_called
    #3
    """


cdef class _getattribute:
    cdef int getattribute_called
    def __getattribute__(self,n):
        self.getattribute_called += 1
        if n == 'resolved_by':
            return '_getattribute'
        elif n == '_getattribute':
            return True
        elif n == 'getattribute_called':
            return self.getattribute_called
        else:
            raise AttributeError


class getattribute_py(_getattribute):
    """
    getattribute is inherited.

    >>> a = getattribute_py()
    >>> a.getattribute_called
    1
    >>> print(a.resolved_by)
    _getattribute
    >>> a.getattribute_called
    3
    >>> print(a._getattribute)
    True
    >>> a.getattribute_called
    5
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    7
    """


cdef class boring_getattribute(_getattribute):
    cdef readonly int boring_getattribute_member

cdef class boring_boring_getattribute(boring_getattribute):
    """
    getattribute is inherited.

    >>> a = boring_boring_getattribute()
    >>> a.getattribute_called
    1
    >>> try: a.boring_getattribute_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    3
    >>> try: a.boring_boring_getattribute_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    5
    >>> print(a.resolved_by)
    _getattribute
    >>> a.getattribute_called
    7
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> a.getattribute_called
    9
    """
    cdef readonly int boring_boring_getattribute_member


class boring_boring_getattribute_py(boring_boring_getattribute):
    __doc__ = boring_boring_getattribute.__doc__.replace(
        'boring_boring_getattribute()', 'boring_boring_getattribute_py()')


cdef class boring_getattr(_getattr):
    cdef readonly int boring_getattr_member

cdef class boring_boring_getattr(boring_getattr):
    cdef readonly int boring_boring_getattr_member

cdef class getattribute_boring_boring_getattr(boring_boring_getattr):
    """
    __getattribute__ is always tried first, then __getattr__, regardless of where
    in the inheritance hierarchy they came from.

    >>> a = getattribute_boring_boring_getattr()
    >>> (a.getattr_called, a.getattribute_called)
    (1, 2)
    >>> print(a.resolved_by)
    getattribute_boring_boring_getattr
    >>> (a.getattr_called, a.getattribute_called)
    (2, 5)
    >>> a.getattribute_boring_boring_getattr
    True
    >>> (a.getattr_called, a.getattribute_called)
    (3, 8)
    >>> a._getattr
    True
    >>> (a.getattr_called, a.getattribute_called)
    (5, 11)
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> (a.getattr_called, a.getattribute_called)
    (7, 14)
    """
    cdef int getattribute_called
    def __getattribute__(self,n):
        self.getattribute_called += 1
        if n == 'resolved_by':
            return 'getattribute_boring_boring_getattr'
        elif n == 'getattribute_boring_boring_getattr':
            return True
        elif n == 'getattribute_called':
            return self.getattribute_called
        else:
            raise AttributeError


# currently fails, see #1793
#class getattribute_boring_boring_getattr_py(getattribute_boring_boring_getattr):
#    __doc__ = getattribute_boring_boring_getattr.__doc__.replace(
#        'getattribute_boring_boring_getattr()', 'getattribute_boring_boring_getattr_py()')


cdef class getattr_boring_boring_getattribute(boring_boring_getattribute):
    """
    __getattribute__ is always tried first, then __getattr__, regardless of where
    in the inheritance hierarchy they came from.

    >>> a = getattr_boring_boring_getattribute()
    >>> (a.getattr_called, a.getattribute_called)
    (1, 2)
    >>> print(a.resolved_by)
    _getattribute
    >>> (a.getattr_called, a.getattribute_called)
    (2, 5)
    >>> a.getattr_boring_boring_getattribute
    True
    >>> (a.getattr_called, a.getattribute_called)
    (4, 8)
    >>> a._getattribute
    True
    >>> (a.getattr_called, a.getattribute_called)
    (5, 11)
    >>> try: a.no_such_member
    ... except AttributeError: pass
    ... else: print("FAILED!")
    >>> (a.getattr_called, a.getattribute_called)
    (7, 14)
    """
    cdef readonly int getattr_called  # note: property will not be used due to __getattribute__()
    def __getattr__(self,n):
        self.getattr_called += 1
        if n == 'resolved_by':
            return 'getattr_boring_boring_getattribute'
        elif n == 'getattr_boring_boring_getattribute':
            return True
        elif n == 'getattr_called':
            return self.getattr_called
        else:
            raise AttributeError


# currently fails, see #1793
#class getattr_boring_boring_getattribute_py(getattr_boring_boring_getattribute):
#    __doc__ = getattr_boring_boring_getattribute.__doc__.replace(
#        'getattr_boring_boring_getattribute()', 'getattr_boring_boring_getattribute_py()')
