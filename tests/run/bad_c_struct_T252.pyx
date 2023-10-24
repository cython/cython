# ticket: t252

fn cf(default=None):
    return default

cpdef cpf(default=100):
    """
    >>> cpf()
    100
    >>> cpf(1)
    1
    >>> cpf(default=2)
    2
    """
    default = cf(default)
    return default

def pf(default=100):
    """
    >>> pf()
    100
    >>> pf(1)
    1
    >>> pf(default=2)
    2
    """
    return default

struct foo:
    i32 void
    i32 default

def test_struct():
    """
    >>> test_struct()
    (1, 2)
    """
    let foo foo_struct
    foo_struct.void = 1
    foo_struct.default = 2
    return foo_struct.void, foo_struct.default

cdef class Foo:
    cdef i32 void
    cdef i32 default

def test_class():
    """
    >>> test_class()
    (1, 2)
    """
    let Foo foo_instance = Foo()
    foo_instance.void = 1
    foo_instance.default = 2
    return foo_instance.void, foo_instance.default
