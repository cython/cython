# mode: run
# tag: closures, cpdef, ccall

"""
Tests for cpdef/ccall functions containing closures (lambda, inner def,
genexpr, comprehensions). Generators are excluded (Part B).
"""

import cython

# ---------------------------------------------------------------------------
# Module-level cpdef with various closure forms
# ---------------------------------------------------------------------------

cpdef int cpdef_with_lambda():
    """
    >>> cpdef_with_lambda()
    1
    """
    f = lambda: 1
    return f()


cpdef object cpdef_with_inner_def():
    """
    >>> cpdef_with_inner_def()
    42
    """
    def inner():
        return 42
    return inner()


cpdef bint cpdef_with_genexpr(values):
    """
    >>> cpdef_with_genexpr([1, 2, 3])
    True
    >>> cpdef_with_genexpr([-1, -2])
    False
    """
    return any(x > 0 for x in values)


cpdef list cpdef_with_listcomp(values):
    """
    >>> cpdef_with_listcomp([1, 2, 3])
    [2, 4, 6]
    """
    return [x * 2 for x in values]


cpdef set cpdef_with_setcomp(values):
    """
    >>> sorted(cpdef_with_setcomp([1, 2, 2, 3]))
    [1, 2, 3]
    """
    return {x for x in values}


cpdef dict cpdef_with_dictcomp(keys, values):
    """
    >>> cpdef_with_dictcomp(['a', 'b'], [1, 2])
    {'a': 1, 'b': 2}
    """
    return {k: v for k, v in zip(keys, values)}


# ---------------------------------------------------------------------------
# @cython.ccall (pure-Python syntax) with lambda — the original crash case
# ---------------------------------------------------------------------------

@cython.ccall
def ccall_with_lambda() -> cython.bint:
    """
    >>> ccall_with_lambda()
    True
    """
    return (lambda: True)()


# ---------------------------------------------------------------------------
# cpdef with optional arg captured by a closure (A4 regression)
# ---------------------------------------------------------------------------

cpdef object cpdef_default_capture(x=1):
    """
    >>> cpdef_default_capture()
    1
    >>> cpdef_default_capture(42)
    42
    """
    return (lambda: x)()


# ---------------------------------------------------------------------------
# Calling cpdef-with-closure from another cpdef (C-to-C call path)
# ---------------------------------------------------------------------------

cpdef int call_cpdef_from_cpdef():
    """
    >>> call_cpdef_from_cpdef()
    1
    """
    return cpdef_with_lambda()


# ---------------------------------------------------------------------------
# cdef class with a cpdef method whose lambda captures self and a typed local
# ---------------------------------------------------------------------------

cdef class Base:
    cpdef int make_value(self, int scale):
        """
        >>> b = Base()
        >>> b.make_value(3)
        9
        """
        cdef int local = scale * scale
        f = lambda: local
        return f()

    cpdef object make_list(self, int n):
        """
        >>> b = Base()
        >>> b.make_list(3)
        [0, 1, 2]
        """
        return [x for x in range(n)]


class PythonDerived(Base):
    """Pure-Python subclass overriding a cpdef method."""
    def make_value(self, scale):
        """
        >>> d = PythonDerived()
        >>> d.make_value(5)
        125
        """
        return scale * scale * scale  # intentionally different to detect dispatch


def test_override_check():
    """
    C call through Base-typed pointer must dispatch to Python override.

    >>> test_override_check()
    125
    """
    cdef Base b = PythonDerived()
    return b.make_value(5)


# ---------------------------------------------------------------------------
# cpdef with lambda capturing self (cdef class method)
# ---------------------------------------------------------------------------

cdef class SelfCapture:
    cdef public int value

    def __init__(self, int v):
        self.value = v

    cpdef int get_value_via_lambda(self):
        """
        >>> obj = SelfCapture(7)
        >>> obj.get_value_via_lambda()
        7
        """
        f = lambda: self.value
        return f()
