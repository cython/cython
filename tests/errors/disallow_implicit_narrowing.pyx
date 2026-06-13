# cython: disallow_implicit_narrowing=True
# mode: error

cdef class Foo:
    pass

ctypedef (int, int) IntPair

def test_narrowing_to_extension_type(object o):
    cdef Foo x = o  # error: object -> extension type

def test_narrowing_to_c_int(object o):
    cdef int x = o  # error: object -> C int

def test_narrowing_to_ctuple(object o):
    cdef IntPair x = o  # error: object -> ctuple

def test_for_loop_exemption(list collection):
    # typed loop var over untyped collection must NOT raise an error
    cdef Foo item
    for item in collection:
        pass

_ERRORS = """
10:17: Implicit narrowing of 'object' to 'Foo' requires an explicit cast (disallow_implicit_narrowing is enabled)
13:17: Implicit narrowing of 'object' to 'int' requires an explicit cast (disallow_implicit_narrowing is enabled)
16:21: Implicit narrowing of 'object' to 'IntPair' requires an explicit cast (disallow_implicit_narrowing is enabled)
"""
