# mode: run
# tag: lambda
# ticket: 605

cdef int cdef_CONST = 123
CONST = 456

cdef class Foo:
    """
    >>> obj = Foo()
    >>> obj.id(123)
    123
    >>> obj.cconst_mul(1)
    123
    >>> obj.const_mul(1)
    456
    >>> obj.foo[0](1)
    1
    """
    id = lambda self, x: x
    cconst_mul = lambda self, x: x * cdef_CONST
    const_mul = lambda self, x: x * CONST
    foo = (lambda x:x,)

class Bar:
    """
    >>> obj = Bar()
    >>> obj.id(123)
    123
    >>> obj.cconst_mul(1)
    123
    >>> obj.const_mul(1)
    456
    >>> obj.foo[0](1)
    1
    """
    id = lambda self, x: x
    cconst_mul = lambda self, x: x * cdef_CONST
    const_mul = lambda self, x: x * CONST
    foo = (lambda x:x,)
