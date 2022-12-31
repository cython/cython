cdef extern from *:
    """
    #ifdef CYTHON_USE_TYPE_SPECS
    #define TYPESPECS 1
    #else
    #define TYPESPECS 0
    #endif
    """
    int TYPESPECS

cdef class Foo:
    """
    >>> D = Foo.__dict__
    >>> D["meth"] is D["meth2"]
    True
    >>> D["classmeth"] is D["classmeth2"]
    True
    >>> D["staticmeth"] is D["staticmeth2"]
    True
    """
    def meth(self): pass
    @classmethod
    def classmeth(cls): pass
    @staticmethod
    def staticmeth(): pass

    meth2 = meth
    classmeth2 = classmeth
    staticmeth2 = staticmeth

cdef class ChangeName:
    # the class seems to need some contents for changing the
    # name to cause a problem
    cdef public str attr1
    cdef public int attr2

if TYPESPECS:
    __doc__ = """
    For typespecs, cdef classes are mutable on some Python versions
    (and it's easiest to leave them that way). Therefore the test
    is just that reassigning the name doesn't cause a crash

    >>> try:
    ...     ChangeName.__name__ = "SomethingElse"
    ... except TypeError:
    ...     pass  # either type error or changing the name is fine
    """
else:
    __doc__ = """
    GH-5079
    Assigning to the cdef class name shouldn't cause a crash.
    The important bit of this test is the not crashing - it's
    possible that typespec/limited-API defined classes will be
    naturally mutable and that isn't a huge problem

    >>> ChangeName.__name__ = "SomethingElse"  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...
    >>> ChangeName.__name__
    'ChangeName'
    """

