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

cdef class C:
    cdef double x
    def __init__(self, x):
        self.x = x

def class_attr_lookup(x):
    """
    >>> class_attr_lookup(C(5))
    5.0
    >>> class_attr_lookup([1])
    >>> class_attr_lookup(None)
    """
    match x:
        case C(x=y):  # This can only work with cdef attribute lookup
            assert cython.typeof(y) == "double", cython.typeof(y)
            return y

class PyClass(object):
    pass

@cython.test_assert_path_exists("//PythonCapiFunctionNode[@cname='__Pyx_TypeCheck']")
def class_typecheck_exists(x):
    """
    Test exists to confirm that the unoptimized case makes an isinstance check
    (and thus the optimized class_typecheck_exists is testing the right thing).
    If the implementation changes to not use a call to "isinstance" this test
    can happily be deleted
    >>> class_typecheck_exists(5)
    False
    >>> class_typecheck_exists(PyClass())
    True
    """
    match x:
        case PyClass():
            return True
        case _:
            return False


@cython.test_fail_if_path_exists("//NameNode[@name='isinstance']")
@cython.test_fail_if_path_exists("//PythonCapiFunctionNode[@cname='__Pyx_TypeCheck']")
def class_typecheck_doesnt_exist(C x):
    """
    >>> class_typecheck_doesnt_exist(C(5))
    True
    >>> class_typecheck_doesnt_exist(None)  # it is None-safe though!
    False
    """
    match x:
        case C():
            return True
        case _:
            return False

def simple_or_with_targets(x):
    """
    This was being mishandled by being converted to an if statement
    without accounting for target assignment
    >>> simple_or_with_targets(1)
    1
    >>> simple_or_with_targets(2)
    2
    >>> simple_or_with_targets(3)
    3
    >>> simple_or_with_targets(4)
    """
    match x:
        case ((1 as y)|(2 as y)|(3 as y)):
            return y
