# cython: disallow_implicit_narrowing=True

"""
Test that with disallow_implicit_narrowing=True, explicit casts still compile
and work correctly, and that for-loop iteration over untyped collections is allowed.
"""

cdef class Foo:
    cdef public int value
    def __init__(self, int v):
        self.value = v


def test_explicit_cast_works():
    """
    >>> f = test_explicit_cast_works()
    >>> type(f).__name__
    'Foo'
    >>> f.value
    42
    """
    cdef object o = Foo(42)
    cdef Foo x = <Foo>o  # explicit cast: no error
    return x


def test_explicit_cast_c_int():
    """
    >>> test_explicit_cast_c_int()
    7
    """
    cdef object o = 7
    cdef int x = <int>o  # explicit cast: no error
    return x


def test_object_to_object_no_error():
    """
    >>> test_object_to_object_no_error()
    'hello'
    """
    cdef object o = "hello"
    cdef object x = o  # object -> object: not narrowing, no error
    return x


def test_for_loop_over_untyped_collection(list collection):
    """
    >>> test_for_loop_over_untyped_collection([Foo(1), Foo(2), Foo(3)])
    [1, 2, 3]
    """
    # typed loop var over untyped (object-yielding) collection: must not error
    cdef Foo item
    cdef list result = []
    for item in collection:
        result.append(item.value)
    return result
