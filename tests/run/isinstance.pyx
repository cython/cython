
cimport cython
from cpython.bool cimport bool

cdef class A:
    pass

@cython.test_assert_path_exists('//SimpleCallNode//SimpleCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode//PythonCapiCallNode',
                                 '//PythonCapiCallNode//SimpleCallNode')
def test_non_optimised():
    """
    >>> test_non_optimised()
    True
    """
    # Non-optimized
    cdef object foo = A
    assert isinstance(A(), foo)
    assert isinstance(0, (int, long))
    assert not isinstance(u"xyz", (int, long))
    return True

@cython.test_assert_path_exists('//PythonCapiCallNode',
                                '//PythonCapiCallNode//SimpleCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode//SimpleCallNode',
                                 '//SimpleCallNode//PythonCapiCallNode')
def test_optimised():
    """
    >>> test_optimised()
    True
    """
    new_type = type('a',(),{})

    # Optimized tests.
    assert isinstance(new_type, type)
    assert isinstance(True, bool)
    assert isinstance(int(), int)
    assert isinstance(long(), long)
    assert isinstance(float(), float)
    assert isinstance(bytes(), bytes)
    assert isinstance(str(), str)
    assert isinstance(unicode(), unicode)
    assert isinstance(tuple(), tuple)
    assert isinstance(list(), list)
    assert isinstance(dict(), dict)
    assert isinstance(set(), set)
    assert isinstance(slice(0), slice)
    assert isinstance(complex(), complex)
    assert not isinstance(u"foo", int)
    assert isinstance(A, type)
    assert isinstance(A(), A)
    cdef type typed_type = A
    assert isinstance(A(), typed_type)
    cdef object untyped_type = A
    assert isinstance(A(), <type>untyped_type)
    return True

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode//SimpleCallNode',
                                 '//SimpleCallNode//PythonCapiCallNode',
                                 '//TupleNode//NameNode')
def test_optimised_tuple():
    """
    >>> test_optimised_tuple()
    True
    """
    assert isinstance(int(),   (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, A))
    assert isinstance(list(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, A))
    assert isinstance(A(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, A))
    return True

def test_custom():
    """
    >>> test_custom()
    True
    """
    assert isinstance(A(), A)
    return True

cdef class B:
    pass

cdef class C:
    pass

def test_custom_tuple(obj):
    """
    >>> test_custom_tuple(A())
    True
    >>> test_custom_tuple(B())
    True
    >>> test_custom_tuple(C())
    False
    """
    return isinstance(obj, (A,B))

def test_nested(x):
    """
    >>> test_nested(1)
    True
    >>> test_nested(1.5)
    True
    >>> test_nested("a")
    False
    """
    cdef object a = (x, None)
    if isinstance(a[0], (int, float)):
        return True
    return False
