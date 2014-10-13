
cimport cython
from cpython.bool cimport bool

cdef class A:
    pass


a_as_obj = A


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
    return True


@cython.test_assert_path_exists('//PythonCapiCallNode',
                                '//PythonCapiCallNode//SimpleCallNode',
                                '//PythonCapiFunctionNode[@cname = "PyType_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyInt_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyFloat_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyBytes_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyUnicode_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyTuple_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyList_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyDict_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PySet_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PySlice_Check"]',
                                '//PythonCapiFunctionNode[@cname = "PyComplex_Check"]')
@cython.test_fail_if_path_exists('//SimpleCallNode//SimpleCallNode',
                                 '//SimpleCallNode//PythonCapiCallNode')
def test_optimised():
    """
    >>> test_optimised()
    True
    """
    # Optimized tests.
    cdef object new_type = type('a',(),{})
    assert isinstance(type('a',(),{}), type)
    assert isinstance(new_type, type)

    cdef object boolval = True
    assert isinstance(boolval, bool)
    assert isinstance(True, bool)

    cdef object intval = int()
    assert isinstance(intval, int)
    assert isinstance(int(), int)

    cdef object longval = long()
    assert isinstance(longval, long)
    assert isinstance(long(), long)

    cdef object floatval = float()
    assert isinstance(floatval, float)
    assert isinstance(float(), float)

    cdef object bytesval = bytes()
    assert isinstance(bytesval, bytes)
    assert isinstance(bytes(), bytes)

    cdef object strval = str()
    assert isinstance(strval, str)
    assert isinstance(str(), str)

    cdef object unicodeval = unicode()
    assert isinstance(unicodeval, unicode)
    assert isinstance(unicode(), unicode)

    cdef object tupleval = tuple()
    assert isinstance(tupleval, tuple)
    assert isinstance(tuple(), tuple)

    cdef object listval = list()
    assert isinstance(listval, list)
    assert isinstance(list(), list)

    cdef object dictval = dict()
    assert isinstance(dictval, dict)
    assert isinstance(dict(), dict)

    cdef object setval = set()
    assert isinstance(setval, set)
    assert isinstance(set(), set)

    cdef object sliceval = slice(0)
    assert isinstance(sliceval, slice)
    assert isinstance(slice(0), slice)

    cdef object complexval = complex()
    assert isinstance(complexval, complex)
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
    assert isinstance(int(),   (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(list(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(A(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(A(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A, a_as_obj))
    assert isinstance(A(),  (int, long, float, bytes, str, unicode, tuple, list, dict, set, slice, type, a_as_obj, A))
    assert isinstance(A(),  (int, long, float, bytes, str, unicode, a_as_obj, tuple, list, dict, set, slice, type, A))
    assert isinstance(0, (int, long))
    assert not isinstance(u"xyz", (int, long))
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


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode//SimpleCallNode',
                                 '//SimpleCallNode//PythonCapiCallNode',
                                 '//TupleNode//NameNode')
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
