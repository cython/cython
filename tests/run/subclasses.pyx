cdef class Base0:
    pass

cdef class Base(Base0):
    pass

cdef class Foo(Base):
   cdef fooit(self):
       return 42

cdef class Bar(Foo):
   pass

cdef class Bam(Bar):
   pass

cdef class Zoo(Bam):
   pass


def fooit(Foo foo):
    """
    >>> zoo = Zoo()
    >>> for cl in (Zoo, Bam, Bar, Foo, Base, Base0): assert isinstance(zoo, cl)
    >>> fooit(zoo)
    42
    >>> bam = Bam()
    >>> for cl in (Bam, Bar, Foo, Base, Base0): assert isinstance(bam, cl)
    >>> fooit(bam)
    42
    >>> bar = Bar()
    >>> for cl in (Bar, Foo, Base, Base0): assert isinstance(bar, cl)
    >>> fooit(bar)
    42
    >>> foo = Foo()
    >>> for cl in (Foo, Base, Base0): assert isinstance(foo, cl)
    >>> fooit(foo)
    42
    >>> base = Base()
    >>> for cl in (Base, Base0): assert isinstance(base, cl)
    >>> fooit(base)
    Traceback (most recent call last):
    TypeError: Argument 'foo' has incorrect type (expected subclasses.Foo, got subclasses.Base)
    >>> base0 = Base0()
    >>> for cl in (Base0,): assert isinstance(base0, cl)
    >>> fooit(base0)
    Traceback (most recent call last):
    TypeError: Argument 'foo' has incorrect type (expected subclasses.Foo, got subclasses.Base0)
    """
    return foo.fooit()
