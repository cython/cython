# cython: legacy_implicit_noexcept=True
# mode: run
# tag: warnings
import sys
import functools
import cython
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

cdef int func_implicit(int a, int b):
    raise RuntimeError

cdef int func_noexcept(int a, int b) noexcept:
    raise RuntimeError

cdef int func_star(int a, int b) except *:
    raise RuntimeError

cdef int func_value(int a, int b) except -1:
    raise RuntimeError

cdef func_return_obj_implicit(int a, int b):
    raise RuntimeError

cdef int(*ptr_func_implicit)(int, int)
ptr_func_implicit = func_implicit

cdef int(*ptr_func_noexcept)(int, int) noexcept
ptr_func_noexcept = func_noexcept

# tests checking that following warning does not occur:
# noexcept clause is ignored for function returning Python object

cdef object test_noexcept_warning_object(x):
    return x

cdef str test_noexcept_warning_str():
    return 'a'

cdef test_noexcept_warning():
    pass

@cython.cfunc
def func_pure_implicit() -> cython.int:
    raise RuntimeError

@cython.exceptval(check=False)
@cython.cfunc
def func_pure_noexcept() -> cython.int:
    raise RuntimeError

def print_stderr(func):
    @functools.wraps(func)
    def testfunc():
        from contextlib import redirect_stderr
        with redirect_stderr(sys.stdout):
            func()

    return testfunc

@print_stderr
def test_noexcept():
    """
    >>> test_noexcept()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_noexcept(3, 5)

@print_stderr
def test_ptr_noexcept():
    """
    >>> test_ptr_noexcept()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    ptr_func_noexcept(3, 5)

@print_stderr
def test_implicit():
    """
    >>> test_implicit()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_implicit(1, 2)

@print_stderr
def test_ptr_implicit():
    """
    >>> test_ptr_implicit()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    ptr_func_implicit(1, 2)

def test_star():
    """
    >>> test_star()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_star(1, 2)

def test_value():
    """
    >>> test_value()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_value(1, 2)


def test_return_obj_implicit():
    """
    >>> test_return_obj_implicit()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_return_obj_implicit(1, 2)

@print_stderr
def test_pure_implicit():
    """
    >>> test_pure_implicit()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_pure_implicit()

@print_stderr
def test_pure_noexcept():
    """
    >>> test_pure_noexcept()  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_pure_noexcept()

# extern functions are implicit noexcept, without warning
cdef extern int extern_fun()
cdef extern int extern_fun_fun(int (*f)(int))


_WARNINGS = """
12:0: Unraisable exception in function 'legacy_implicit_noexcept.func_implicit'.
12:22: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
15:0: Unraisable exception in function 'legacy_implicit_noexcept.func_noexcept'.
27:28: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
45:0: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
45:0: Unraisable exception in function 'legacy_implicit_noexcept.func_pure_implicit'.
49:0: Unraisable exception in function 'legacy_implicit_noexcept.func_pure_noexcept'.
"""
