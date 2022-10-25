# cython: legacy_implicit_noexcept=True
# mode: run
# tag: warnings
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

@cython.cfunc
def pure_func_implicit():
    raise RuntimeError

def test_noexcept():
    """
    >>> print(test_noexcept())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    import sys
    old_stderr = sys.stderr
    stderr = sys.stderr = StringIO()
    try:
        func_noexcept(3, 5)
    finally:
        sys.stderr = old_stderr
    return stderr.getvalue().strip()

def test_ptr_noexcept():
    """
    >>> print(test_ptr_noexcept())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    import sys
    old_stderr = sys.stderr
    stderr = sys.stderr = StringIO()
    try:
        ptr_func_noexcept(3, 5)
    finally:
        sys.stderr = old_stderr
    return stderr.getvalue().strip()

def test_implicit():
    """
    >>> print(test_implicit())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    import sys
    old_stderr = sys.stderr
    stderr = sys.stderr = StringIO()
    try:
        func_implicit(1, 2)
    finally:
        sys.stderr = old_stderr
    return stderr.getvalue().strip()

def test_ptr_implicit():
    """
    >>> print(test_ptr_implicit())  # doctest: +ELLIPSIS
    RuntimeError
    Exception...ignored...
    """
    import sys
    old_stderr = sys.stderr
    stderr = sys.stderr = StringIO()
    try:
        ptr_func_implicit(1, 2)
    finally:
        sys.stderr = old_stderr
    return stderr.getvalue().strip()

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
    pure_func_implicit()

_WARNINGS = """
10:5: Unraisable exception in function 'legacy_implicit_noexcept.func_implicit'.
10:36: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
13:5: Unraisable exception in function 'legacy_implicit_noexcept.func_noexcept'.
22:43: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
25:38: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
"""
