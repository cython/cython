# mode: run
# tag: exttype, final

cimport cython

cdef class TopBase:
    cdef method(self):
        return None


cdef class BaseClass(TopBase):
    """
    >>> obj = BaseClass()
    >>> obj.call_base()
    'base'
    """
    cdef base(self):
        return '@base'

    cdef method(self):
        return 'base'

    def call_base(self):
        return self.method()


@cython.final
cdef class ChildClass(BaseClass):
    """
    >>> obj = ChildClass()
    >>> obj.call_base()
    'child'
    >>> obj.call_child()
    'child'
    """
    cdef child(self):
        return '@child'

    cdef method(self):
        return 'child'

    def call_child(self):
        # original bug: this requires a proper cast for self
        return self.method()


def test_BaseClass():
    """
    >>> test_BaseClass()
    '@base'
    'base'
    """
    cdef BaseClass obj = BaseClass()
    print(repr(obj.base()))
    print(repr(obj.method()))


def test_ChildClass():
    """
    >>> test_ChildClass()
    '@base'
    '@child'
    'child'
    '@base'
    '@child'
    'child'
    """
    cdef ChildClass obj = ChildClass()
    print(repr(obj.base()))
    print(repr(obj.child()))
    print(repr(obj.method()))
    cdef BaseClass bobj = obj
    print(repr(obj.base()))
    print(repr(obj.child()))
    print(repr(bobj.method()))
