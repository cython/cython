# mode: run
# tag: nogil
# cython: language_level=2

cimport cython


@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//GILStatNode",
    "//GILStatNode//GILStatNode//PrintStatNode",
)
def test_print_in_nogil(x):
    """
    >>> test_print_in_nogil(123)
    --123--
    """
    with nogil:
        print f"--{x}--"


@cython.test_assert_path_exists(
    "//GILStatNode",
    "//GILStatNode//GILStatNode",
    "//GILStatNode//GILStatNode//RaiseStatNode",
)
def test_raise_in_nogil(x):
    """
    >>> try: test_raise_in_nogil(123)
    ... except ValueError as exc: print(exc)
    ... else: print("NOT RAISED !")
    --123--
    """
    with nogil:
        raise ValueError(f"--{x}--")
