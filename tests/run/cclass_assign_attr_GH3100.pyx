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
    """
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

    # the class seems to need some contents for changing the
    # name to cause a problem
    cdef public str attr1
    cdef public int attr2
