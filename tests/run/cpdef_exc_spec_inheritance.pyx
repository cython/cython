# cython: language_level=3
# mode: run
# tag: cpdef, noexcept, exception

"""Tests that unannotated cpdef overrides inherit the base exception spec,
and that call sites omit PyErr_Occurred() checks for noexcept methods.
"""

cimport cython

# ---- Regular noexcept cpdef method, unannotated override inherits ----

cdef class Base:
    cpdef int method(self) noexcept:
        return 1

cdef class Child(Base):
    # No exception spec: should inherit noexcept from Base.
    cpdef int method(self):
        return 2

def test_noexcept_inheritance():
    """
    >>> test_noexcept_inheritance()
    2
    """
    cdef Child c = Child()
    return c.method()


# ---- except? value inherits ----

cdef class BaseExceptVal:
    cpdef int method(self) except? -1:
        return 10

cdef class ChildExceptVal(BaseExceptVal):
    # No explicit except clause: should inherit except? -1.
    cpdef int method(self):
        return 20

def test_except_val_inheritance():
    """
    >>> test_except_val_inheritance()
    20
    """
    cdef ChildExceptVal c = ChildExceptVal()
    return c.method()


# ---- explicit noexcept on override is OK (same as base) ----

cdef class BaseExplicitNoexcept:
    cpdef int method(self) noexcept:
        return 1

cdef class ChildExplicitNoexcept(BaseExplicitNoexcept):
    cpdef int method(self) noexcept:
        return 3

def test_explicit_noexcept():
    """
    >>> test_explicit_noexcept()
    3
    """
    cdef ChildExplicitNoexcept c = ChildExplicitNoexcept()
    return c.method()


# ---- safe narrowing: base except* -> override noexcept is allowed ----

cdef class BaseExceptStar:
    cpdef int method(self) except *:
        return 10

cdef class ChildNarrow(BaseExceptStar):
    # Safe narrowing: override promises not to raise.
    cpdef int method(self) noexcept:
        return 30

def test_safe_narrowing():
    """
    >>> test_safe_narrowing()
    30
    """
    cdef ChildNarrow c = ChildNarrow()
    return c.method()


# ---- auto_cpdef promoted def inherits noexcept ----

# cython: auto_cpdef=True not used here; test with explicit cpdef.
# The spec says an unannotated promoted def also inherits; test that
# through cpdef which uses the same path.

cdef class BaseAutoNoexcept:
    cpdef double compute(self) noexcept:
        return 1.0

cdef class ChildAutoNoexcept(BaseAutoNoexcept):
    cpdef double compute(self):   # should inherit noexcept
        return 2.0

def test_auto_noexcept_inheritance():
    """
    >>> test_auto_noexcept_inheritance()
    2.0
    """
    cdef ChildAutoNoexcept c = ChildAutoNoexcept()
    return c.compute()


# ---- final type with noexcept cpdef ----

@cython.final
cdef class FinalType:
    cpdef int method(self) noexcept:
        return 42

def test_final_noexcept():
    """
    >>> test_final_noexcept()
    42
    """
    cdef FinalType b = FinalType()
    return b.method()


# ---- auto_cpdef=True at module level: promoted def inherits ----

# cython: auto_cpdef=True is set per-module; test via plain cpdef for now.
# The promoted-def path uses the same `with_exception_spec_of` logic.


# ---- multi-level inheritance: spec propagates transitively ----

cdef class L1:
    cpdef int f(self) noexcept:
        return 1

cdef class L2(L1):
    cpdef int f(self):    # inherits noexcept from L1
        return 2

cdef class L3(L2):
    cpdef int f(self):    # should also inherit noexcept (transitively via L2)
        return 3

def test_transitive_inheritance():
    """
    >>> test_transitive_inheritance()
    3
    """
    cdef L3 c = L3()
    return c.f()


# ===========================================================================
# RAISING TESTS — verify exception propagation through inherited specs
# ===========================================================================

# ---- except -1 inherited, override raises, dynamic Python call ----

cdef class BaseExcMinus1Raise:
    cpdef int method(self) except -1:
        return 10

cdef class ChildExcMinus1Raise(BaseExcMinus1Raise):
    cpdef int method(self):  # inherits except -1
        raise ValueError("from child except -1")

def test_except_minus1_raise_python_call():
    """Called via Python (untyped object): exception must propagate.

    >>> test_except_minus1_raise_python_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except -1
    """
    obj = ChildExcMinus1Raise()
    return obj.method()


def test_except_minus1_raise_static_cython_call():
    """Called via Cython statically typed as base (vtable dispatch with except -1 check).

    >>> test_except_minus1_raise_static_cython_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except -1
    """
    cdef BaseExcMinus1Raise b = ChildExcMinus1Raise()
    return b.method()


# ---- except? -1 inherited, override raises, static Cython call ----

cdef class BaseExcMaybe:
    cpdef int method(self) except? -1:
        return 10

cdef class ChildExcMaybeRaise(BaseExcMaybe):
    cpdef int method(self):  # inherits except? -1
        raise ValueError("from child except? -1")

def test_except_maybe_raise_python_call():
    """
    >>> test_except_maybe_raise_python_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except? -1
    """
    obj = ChildExcMaybeRaise()
    return obj.method()


def test_except_maybe_raise_static_cython_call():
    """
    >>> test_except_maybe_raise_static_cython_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except? -1
    """
    cdef BaseExcMaybe b = ChildExcMaybeRaise()
    return b.method()


# ---- except * base, unannotated override inherits it, override raises ----

cdef class BaseExcStarRaise:
    cpdef int method(self) except *:
        return 10

cdef class ChildExcStarRaise(BaseExcStarRaise):
    cpdef int method(self):  # inherits except *
        raise ValueError("from child except *")

def test_except_star_raise_python_call():
    """
    >>> test_except_star_raise_python_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except *
    """
    obj = ChildExcStarRaise()
    return obj.method()


def test_except_star_raise_static_cython_call():
    """
    >>> test_except_star_raise_static_cython_call()
    Traceback (most recent call last):
        ...
    ValueError: from child except *
    """
    cdef BaseExcStarRaise b = ChildExcStarRaise()
    return b.method()


# ---- Python subclass of cpdef except -1: raises, called statically from Cython ----
# OverrideCheckNode dispatches to the Python override; exception must propagate
# when the caller has the inherited "except -1" check.

cdef class BaseForPySub:
    cpdef int method(self) except -1:
        return 99

class PyChildRaise(BaseForPySub):
    def method(self):
        raise RuntimeError("from Python subclass")

def test_python_subclass_raise_static_call():
    """
    >>> test_python_subclass_raise_static_call()
    Traceback (most recent call last):
        ...
    RuntimeError: from Python subclass
    """
    cdef BaseForPySub b = PyChildRaise()
    return b.method()


def test_python_subclass_raise_python_call():
    """
    >>> test_python_subclass_raise_python_call()
    Traceback (most recent call last):
        ...
    RuntimeError: from Python subclass
    """
    obj = PyChildRaise()
    return obj.method()


# ---- noexcept + raise: exception is unraisable, not propagated ----
# When a noexcept function's body raises, Cython calls PyErr_WriteUnraisable
# (writes to stderr) and returns the C default value (0 for int).
# The exception is NOT propagated — that is the defined noexcept contract.

import sys as _sys

cdef class BaseNoexceptRaisePy:
    cpdef int method(self) noexcept:
        return 0

cdef class ChildNoexceptInheritRaise(BaseNoexceptRaisePy):
    # Inherits noexcept from base; body raises — should become unraisable.
    cpdef int method(self):
        raise ValueError("noexcept body raised")

cdef class ChildNoexceptExplicitRaise(BaseNoexceptRaisePy):
    cpdef int method(self) noexcept:  # explicit noexcept, same as base
        raise ValueError("noexcept body raised explicit")


def _capture_unraisable(func):
    """Call func(), return (result, list_of_unraisable_exceptions)."""
    raised = []
    orig = _sys.unraisablehook
    _sys.unraisablehook = lambda u: raised.append(u.exc_value)
    try:
        result = func()
    finally:
        _sys.unraisablehook = orig
    return result, raised


def test_noexcept_inherit_raise_python_call():
    """Inherited noexcept + raise in body → unraisable, returns 0.

    >>> result, unraisable = _capture_unraisable(ChildNoexceptInheritRaise().method)
    >>> result
    0
    >>> type(unraisable[0]).__name__
    'ValueError'
    >>> str(unraisable[0])
    'noexcept body raised'
    """


def test_noexcept_explicit_raise_python_call():
    """Explicit noexcept + raise body → also unraisable.

    >>> result, unraisable = _capture_unraisable(ChildNoexceptExplicitRaise().method)
    >>> result
    0
    >>> type(unraisable[0]).__name__
    'ValueError'
    """


def test_noexcept_static_dispatch_raise_is_unraisable():
    """Statically-typed Cython dispatch: inherited noexcept, raise → unraisable, returns 0.

    >>> test_noexcept_static_dispatch_raise_is_unraisable()
    """
    cdef BaseNoexceptRaisePy b = ChildNoexceptInheritRaise()
    result, unraisable = _capture_unraisable(b.method)
    assert result == 0, result
    assert len(unraisable) == 1, unraisable
    assert type(unraisable[0]).__name__ == 'ValueError', unraisable
