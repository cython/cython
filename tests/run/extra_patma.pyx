# mode: run

# Extra pattern matching test for Cython-specific features, optimizations, etc.

cimport cython

import array
import sys

__doc__ = ""


cdef bint is_null(int* x):
    return False # disabled - currently just a parser test
    match x:
        case NULL:
            return True
        case _:
            return False


def test_is_null():
    """
    >>> test_is_null()
    """
    cdef int some_int = 1
    return  # disabled - currently just a parser test
    assert is_null(&some_int) == False
    assert is_null(NULL) == True


if sys.version_info[0] > 2:
    __doc__ += """
    array.array doesn't have the buffer protocol in Py2 and
    this doesn't really feel worth working around to test
    >>> print(test_memoryview(array.array('i', [0, 1, 2])))
    a 1
    >>> print(test_memoryview(array.array('i', [])))
    b
    >>> print(test_memoryview(array.array('i', [5])))
    c [5]
    """

# goes via .shape instead
@cython.test_fail_if_path_exists("//CallNode//NameNode[@name = 'len']")
# No need for "is Sequence check"
@cython.test_fail_if_path_exists("//PythonCapiCallNode//PythonCapiFunctionNode[@cname = '__Pyx_MatchCase_IsSequence']")
def test_memoryview(int[:] x):
    """
    >>> print(test_memoryview(None))
    no!
    """
    match x:
        case [0, y, 2]:
            assert cython.typeof(y) == "int", cython.typeof(y)  # type inference works
            return f"a {y}"
        case []:
            return "b"
        case [*z]:
            return f"c {z}"
    return "no!"

@cython.test_fail_if_path_exists("//PythonCapiCallNode//PythonCapiFunctionNode[@cname = '__Pyx_MatchCase_IsSequence']")
def test_list_to_sequence(list x):
    """
    >>> test_list_to_sequence([1,2,3])
    True
    >>> test_list_to_sequence(None)
    False
    """
    match x:
        case [*_]:
            return True
        case _:
            return False


@cython.test_fail_if_path_exists("//PythonCapiCallNode//PythonCapiFunctionNode[@cname = '__Pyx_MatchCase_IsSequence']")
@cython.test_fail_if_path_exists("//CmpNode")  # There's nothing to compare - it always succeeds!
def test_list_not_None_to_sequence(list x not None):
    """
    >>> test_list_not_None_to_sequence([1,2,3])
    True
    """
    match x:
        case [*_]:
            return True
        case _:
            return False

@cython.test_fail_if_path_exists("//PythonCapiCallNode//PythonCapiFunctionNode[@cname = '__Pyx_MatchCase_IsSequence']")
@cython.test_fail_if_path_exists("//CmpNode")  # There's nothing to compare - it always succeeds!
def test_ctuple_to_sequence((int, int) x):
    """
    >>> test_ctuple_to_sequence((1, 2))
    (1, 2)
    """
    match x:
        case [a, b, c]:  # can't possibly succeed!
            return a, b, c
        case [a, b]:
            assert cython.typeof(a) == "int", cython.typeof(a)  # test that types have inferred
            return a, b

