# cython: legacy_implicit_noexcept=True
# mode: run
# tag: warnings

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

def test_star():
    """
    >>> test_star()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_star(1, 2)

_WARNINGS = """
10:5: Unraisable exception in function 'legacy_implicit_noexcept.func_implicit'.
10:36: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
13:5: Unraisable exception in function 'legacy_implicit_noexcept.func_noexcept'.
"""
