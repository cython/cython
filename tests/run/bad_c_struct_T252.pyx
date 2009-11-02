cdef cf(default=None):
    return default

cpdef cpf(default=None):
    """
    >>> cpf()
    None
    >>> cpf(1)
    1
    >>> cpf(default=2)
    2
    """
    default = cf(default)
    return default

def pf(default=None):
    """
    >>> pf()
    None
    >>> pf(1)
    1
    >>> pf(default=2)
    2
    """
    return default


cdef struct foo:
    int void
    int default

def test_struct():
    """
    >>> test_struct()
    (1, 2)
    """
    cdef foo foo_struct
    foo_struct.void = 1
    foo_struct.default = 2
    return foo_struct.void, foo_struct.default


cdef class Foo:
    cdef int void
    cdef int default

def test_class():
    """
    >>> test_class()
    (1, 2)
    """
    cdef Foo foo_instance = Foo()
    foo_instance.void = 1
    foo_instance.default = 2
    return foo_instance.void, foo_instance.default
