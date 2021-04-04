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
