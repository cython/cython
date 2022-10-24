# cython: legacy_implicit_noexcept=True
# mode: run
# tag: warnings

cdef int func_implicit(int a, int b):
    raise RuntimeError

cdef int func_noexcept(int a, int b) noexcept:
    raise RuntimeError

cdef int func_star(int a, int b) except *:
    raise RuntimeError

def test_noexcept():
    """
    >>> test_noexcept()
    """
    func_noexcept(3, 5)

def test_implicit():
    """
    >>> test_implicit()
    """
    func_implicit(1, 2)

def test_star():
    """
    >>> test_star()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    func_star(1, 2)

_WARNINGS = """
5:5: Unraisable exception in function 'legacy_implicit_noexcept.func_implicit'.
5:36: Implicit noexcept declaration is deprecated. Function declaration should contain 'noexcept' keyword.
8:5: Unraisable exception in function 'legacy_implicit_noexcept.func_noexcept'.
"""
