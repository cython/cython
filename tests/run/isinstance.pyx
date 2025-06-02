
cimport cython
from cpython.bool cimport bool

cdef class A:
    pass


a_as_obj = A


@cython.test_assert_path_exists(
    '//SimpleCallNode',
    '//PyMethodCallNode',
    '//SimpleCallNode//PyMethodCallNode',
)
@cython.test_fail_if_path_exists(
    "//PythonCapiCallNode",
)
def test_non_optimised():
    """
    >>> test_non_optimised()
    True
    """
    # Non-optimized
    cdef object foo = A
    assert isinstance(A(), foo)
    return True


@cython.test_assert_path_exists(
    '//PythonCapiCallNode',
    '//PyMethodCallNode',
    '//PythonCapiCallNode//PyMethodCallNode',
    '//PythonCapiFunctionNode[@cname = "PyType_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyLong_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyFloat_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyBytes_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyUnicode_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyTuple_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyList_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyDict_Check"]',
    '//PythonCapiFunctionNode[@cname = "PySet_Check"]',
    '//PythonCapiFunctionNode[@cname = "PySlice_Check"]',
    '//PythonCapiFunctionNode[@cname = "PyComplex_Check"]',
)
@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
)
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
    assert not isinstance(u"xyz", int)

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
    assert isinstance(int(),   (int, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(list(),  (int, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(A(),  (int, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A))
    assert isinstance(A(),  (int, float, bytes, str, unicode, tuple, list, dict, set, slice, type, A, a_as_obj))
    assert isinstance(A(),  (int, float, bytes, str, unicode, tuple, list, dict, set, slice, type, a_as_obj, A))
    assert isinstance(A(),  (int, float, bytes, str, unicode, a_as_obj, tuple, list, dict, set, slice, type, A))
    assert isinstance(0, (str, int))
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


def test_exceptions(exc):
    """
    >>> test_exceptions(AttributeError('aha'))
    'A:AttributeError'
    >>> test_exceptions(ValueError(123))
    'ValueError'
    >>> test_exceptions(IndexError(321))
    'IndexError'
    >>> test_exceptions(RuntimeError("message"))
    'RuntimeError'
    >>> test_exceptions(OSError("eye oh"))
    'OSError'
    >>> test_exceptions(TypeError("message"))
    'E:TypeError'
    """
    try:
        if exc is not None:
            raise exc
    except ValueError:
        return "ValueError"
    except AttributeError as e:
        return f"A:{type(e).__name__}"
    except Exception as e:
        if isinstance(e, IndexError):
            return "IndexError"
        if isinstance(e, RuntimeError):
            return "RuntimeError"
        if type(e) is OSError:
            return "OSError"
        return f"E:{type(e).__name__}"


def skip_if_less_than_310(f):
    import sys
    if sys.version_info < (3, 10):
        return None
    else:
        return f


@cython.test_fail_if_path_exists(
    "//BitwiseOrNode",
)
def test_union(obj):
    """
    >>> test_union([])
    True
    >>> test_union(())
    True
    >>> test_union(b'hello')
    True
    >>> test_union(None)
    True
    >>> test_union(list)
    False
    >>> test_union(1)
    False
    """
    return isinstance(obj, (list | bytes, tuple, list | None | tuple | bytes, bytes))


cdef object py_bytes = bytes

@cython.test_assert_path_exists(
    "//BitwiseOrNode",
)
@skip_if_less_than_310
def test_union_non_type(obj):
    """
    >>> test_union_non_type([])
    True
    >>> test_union_non_type(())
    True
    >>> test_union_non_type(b'hello')
    True
    >>> test_union_non_type(list)
    False
    >>> test_union_non_type(1)
    False
    """
    return isinstance(obj, (list | py_bytes, tuple))


@cython.test_assert_path_exists(
    "//BitwiseOrNode",
)
def test_initial_double_none(obj):
    """
    >>> test_initial_double_none(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: unsupported operand type...
    """
    return isinstance(obj, None | None | int)


@cython.test_fail_if_path_exists(
    "//BitwiseOrNode",
)
def test_double_none_ok(obj):
    """
    >>> test_double_none_ok(1)
    True
    >>> test_double_none_ok(None)
    True
    """
    return isinstance(obj, int | None | None)


@cython.test_fail_if_path_exists(
    "//BitwiseOrNode",
)
@cython.test_assert_path_exists(
    "//PythonCapiCallNode//ResultRefNode",
)
def test_exttype_or_none(get_obj):
    """
    >>> test_exttype_or_none(A)
    True
    >>> test_exttype_or_none(lambda: None)
    True
    >>> test_exttype_or_none(list)
    False
    """
    return isinstance(get_obj(), A | None)
