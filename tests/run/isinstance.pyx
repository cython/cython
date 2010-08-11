
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
    assert isinstance(complex(), complex)  # FIXME: this should be optimised, too!
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
    assert not isinstance(u"foo", int)
    assert isinstance(A, type)
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
    assert isinstance(int(),   (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice))
    assert isinstance(list(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice))
    return True

@cython.test_assert_path_exists('//SimpleCallNode//SimpleCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode//PythonCapiCallNode',
                                 '//PythonCapiCallNode//SimpleCallNode')
def test_custom():
    """
    >>> test_custom()
    True
    """
    assert isinstance(A(), A)
    return True

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
