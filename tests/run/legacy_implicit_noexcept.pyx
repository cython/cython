# cython: legacy_implicit_noexcept=true
# mode: run
# tag: warnings
import sys
import functools
import cython
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

fn i32 func_implicit(i32 a, i32 b):
    raise RuntimeError

fn i32 func_noexcept(i32 a, i32 b) noexcept:
    raise RuntimeError

fn i32 func_star(i32 a, i32 b) except *:
    raise RuntimeError

fn i32 func_value(i32 a, i32 b) except -1:
    raise RuntimeError

fn func_return_obj_implicit(i32 a, i32 b):
    raise RuntimeError

cdef int(*ptr_func_implicit)(i32, i32)
ptr_func_implicit = func_implicit

cdef int(*ptr_func_noexcept)(i32, i32) noexcept
ptr_func_noexcept = func_noexcept

@cython.cfunc
def func_pure_implicit() -> cython.int:
    raise RuntimeError

@cython.excetval(check=false)
@cython.cfunc
def func_pure_noexcept() -> cython.int:
    raise RuntimeError

def return_stderr(func):
    @functools.wraps(func)
    def testfunc():
        old_stderr = sys.stderr
        stderr = sys.stderr = StringIO()
        try:
            func()
        finally:
            sys.stderr = old_stderr
        return stderr.getvalue().strip()

    return testfunc

@return_stderr
def test_noexcept():
    """
    >>> print(test_noexcept())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_noexcept(3, 5)

@return_stderr
def test_ptr_noexcept():
    """
    >>> print(test_ptr_noexcept())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    ptr_func_noexcept(3, 5)

@return_stderr
def test_implicit():
    """
    >>> print(test_implicit())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    func_implicit(1, 2)

@return_stderr
def test_ptr_implicit():
    """
    >>> print(test_ptr_implicit())  # doctest: +ELLIPSIS
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

def test_pure_implicit():
    """
    >>> test_pure_implicit()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_pure_implicit()

def test_pure_noexcept():
    """
    >>> test_pure_noexcept()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_pure_noexcept()

_WARNINGS = """
12:0: Unraisable exception in function 'legacy_implicit_noexcept.func_implicit'.
12:34: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
15:0: Unraisable exception in function 'legacy_implicit_noexcept.func_noexcept'.
24:41: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
27:38: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
"""
