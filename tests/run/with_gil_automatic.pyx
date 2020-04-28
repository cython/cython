# mode: run
# tag: nogil
# cython: language_level=2

cimport cython


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
cpdef int test_print_in_nogil_func(x) nogil except -1:
    """
    >>> _ = test_print_in_nogil_func(123)
    --123--
    """
    print f"--{x}--"


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
cpdef int test_raise_in_nogil_func(x) nogil except -1:
    """
    >>> try: test_raise_in_nogil_func(123)
    ... except ValueError as exc: print(exc)
    ... else: print("NOT RAISED !")
    --123--
    """
    raise ValueError(f"--{x}--")
