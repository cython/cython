# mode: run
# tag: nogil
# cython: language_level=2

cimport cython

#### print

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//GILStatNode",
    "//GILStatNode//GILStatNode//PrintStatNode",
)
def test_print_in_nogil_section(x):
    """
    >>> test_print_in_nogil_section(123)
    --123--
    """
    with nogil:
        print f"--{x}--"

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//PrintStatNode",
)
@cython.test_fail_if_path_exists(
    "//GILStatNode//GILStatNode",
)
cpdef i32 test_print_in_nogil_func(x) except -1 nogil:
    """
    >>> _ = test_print_in_nogil_func(123)
    --123--
    """
    print f"--{x}--"


#### raise

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//GILStatNode",
    "//GILStatNode//GILStatNode//RaiseStatNode",
)
def test_raise_in_nogil_section(x):
    """
    >>> try: test_raise_in_nogil_section(123)
    ... except ValueError as exc: print(exc)
    ... else: print("NOT RAISED !")
    --123--
    """
    with nogil:
        raise ValueError(f"--{x}--")

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//RaiseStatNode",
)
@cython.test_fail_if_path_exists(
    "//GILStatNode//GILStatNode",
)
cpdef i32 test_raise_in_nogil_func(x) except -1 nogil:
    """
    >>> test_raise_in_nogil_func(123)
    Traceback (most recent call last):
    ValueError: --123--
    """
    raise ValueError(f"--{x}--")

#### assert

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//AssertStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode//RaiseStatNode",
)
def assert_in_nogil_section(i32 x):
    """
    >>> assert_in_nogil_section(123)
    >>> assert_in_nogil_section(0)
    Traceback (most recent call last):
    AssertionError
    """
    with nogil:
        assert x

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//AssertStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode//RaiseStatNode",
)
def assert_in_nogil_section_ustring(i32 x):
    """
    >>> assert_in_nogil_section_string(123)
    >>> assert_in_nogil_section_string(0)
    Traceback (most recent call last):
    AssertionError: failed!
    """
    with nogil:
        assert x, u"failed!"

@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//AssertStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode",
    "//GILStatNode//AssertStatNode//GILStatNode//RaiseStatNode",
)
def assert_in_nogil_section_string(i32 x):
    """
    >>> assert_in_nogil_section_string(123)
    >>> assert_in_nogil_section_string(0)
    Traceback (most recent call last):
    AssertionError: failed!
    """
    with nogil:
        assert x, "failed!"

@cython.test_assert_path_exists(
    "//AssertStatNode",
    "//AssertStatNode//GILStatNode",
    "//AssertStatNode//GILStatNode//RaiseStatNode",
)
cpdef int assert_in_nogil_func(i32 x) except -1 nogil:
    """
    >>> _ = assert_in_nogil_func(123)
    >>> assert_in_nogil_func(0)
    Traceback (most recent call last):
    AssertionError: failed!
    """
    assert x, "failed!"
