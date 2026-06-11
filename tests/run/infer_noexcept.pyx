# cython: language_level=3
# mode: run
# tag: infer_noexcept, optimization

"""Tests for the InferNoexcept compiler pass (directive ``infer_noexcept``, default True).

The pass marks provably non-raising final methods, final property accessors, and
module-level cpdef/cdef functions with ``CFuncType.never_raises = True``, and for
non-pyobject return types also clears exception_check/exception_value so callers skip
post-call PyErr_Occurred() checks.  Pyobject-returning marked functions additionally
suppress the NULL-check at call sites.

Non-final cpdef methods are NEVER tier-1 marked (vtable override safety).
"""

cimport cython
import sys as _sys


# ===========================================================================
# Helpers for capturing unraisable exceptions
# ===========================================================================

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


# ===========================================================================
# TIER-1 POSITIVE CASES — final cdef class
# ===========================================================================

@cython.final
cdef class Point:
    """Final class whose simple accessors should all be inferred never-raising."""
    cdef int _x
    cdef int _y
    cdef object _tag   # PyObject field

    def __init__(self, int x, int y, tag=None):
        self._x = x
        self._y = y
        self._tag = tag

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cdef int get_x(self):
        # Simple C-int getter: tier-1 candidate (final class, safe body).
        return self._x

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cpdef void set_x(self, int v):
        # cpdef void setter: safe body, never raises.
        self._x = v

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cpdef double norm2(self):
        # cpdef double: pure C arithmetic, never raises.
        return self._x * self._x + self._y * self._y

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cdef object get_tag(self):
        # Object-forwarding getter: never_raises flag suppresses NULL-check at caller.
        return self._tag

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cdef void set_tag(self, object v):
        # PyObject-field setter: incref/decref never raise.
        self._tag = v


def test_final_cint_getter():
    """C-int getter on final class: inferred never_raises.

    >>> test_final_cint_getter()
    7
    """
    cdef Point p = Point(7, 3)
    return p.get_x()


def test_final_cpdef_setter():
    """cpdef void setter on final class: inferred never_raises.

    >>> test_final_cpdef_setter()
    99
    """
    cdef Point p = Point(1, 2)
    p.set_x(99)
    return p.get_x()


def test_final_cpdef_norm2():
    """cpdef double on final class: inferred never_raises.

    >>> test_final_cpdef_norm2()
    25.0
    """
    cdef Point p = Point(3, 4)
    return p.norm2()


@cython.test_assert_path_exists(
    "//SimpleCallNode[@function.type.never_raises = True]",
)
def test_final_object_getter():
    """Object-forwarding getter: never_raises suppresses NULL check at caller.

    >>> test_final_object_getter()
    'hello'
    """
    cdef Point p = Point(1, 2, 'hello')
    return p.get_tag()


def test_final_pyobject_setter():
    """PyObject-field setter: incref/decref never raises.

    >>> test_final_pyobject_setter()
    'world'
    """
    cdef Point p = Point(1, 2, 'old')
    p.set_tag('world')
    return p.get_tag()


# ===========================================================================
# TIER-1 POSITIVE CASES — module-level cpdef/cdef functions
# ===========================================================================

@cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int add(int a, int b):
    return a + b

@cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
cdef int csub(int a, int b):
    return a - b


def test_module_cpdef_add():
    """Module-level cpdef: inferred never_raises.

    >>> test_module_cpdef_add()
    5
    """
    return add(2, 3)


def test_module_cdef_csub():
    """Module-level cdef: inferred never_raises.

    >>> test_module_cdef_csub()
    1
    """
    return csub(4, 3)


# ===========================================================================
# TIER-1 POSITIVE — chained calls (callee already never_raises → caller safe)
# ===========================================================================

@cython.test_assert_path_exists(
    "//CFuncDefNode[@type.never_raises = True]",
    "//SimpleCallNode[@function.type.never_raises = True]",
)
cpdef int add_one(int n):
    # Calls add(), which is already inferred never_raises; so add_one is also safe.
    return add(n, 1)


@cython.test_assert_path_exists(
    "//SimpleCallNode[@function.type.never_raises = True]",
)
def test_chain_cint():
    """Chained call through two never_raises functions; callee call site has flag.

    >>> test_chain_cint()
    11
    """
    return add_one(10)


@cython.test_assert_path_exists(
    "//SimpleCallNode[@function.type.never_raises = True]",
)
def test_chain_object_getter():
    """Call to object-forwarding never_raises getter: SimpleCallNode gets the flag.

    >>> test_chain_object_getter()
    'abc'
    """
    cdef Point p = Point(1, 2, 'abc')
    tag = p.get_tag()
    return tag


# ===========================================================================
# TIER-1 POSITIVE — division by nonzero constant
# ===========================================================================

@cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int divide_by_two(int n):
    # Constant divisor: Cython doesn't emit a zerodivision_check node → safe.
    return n // 2


def test_const_division():
    """Division by nonzero constant is provably safe.

    >>> test_const_division()
    5
    """
    return divide_by_two(10)


# ===========================================================================
# TIER-1 POSITIVE — nogil function called under with nogil
# ===========================================================================

cdef int nogil_square(int x) noexcept nogil:
    # Already explicitly noexcept: has_explicit_exc_clause=True → inference pass
    # skips it (user spec is sacred). No tree assertion here.
    return x * x


def test_nogil_safe():
    """Module-level cdef noexcept nogil function: provably never raises.

    >>> test_nogil_safe()
    16
    """
    cdef int result
    with nogil:
        result = nogil_square(4)
    return result


# ===========================================================================
# NEGATIVE — bodies that prevent inference
# ===========================================================================

# --- raise in body ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int raises_explicitly(int x):
    if x < 0:
        raise ValueError("negative")
    return x


def test_negative_raise():
    """Function with raise must NOT be inferred never_raises; still works correctly.

    >>> test_negative_raise()
    5
    """
    return raises_explicitly(5)


def test_negative_raise_exception():
    """
    >>> test_negative_raise_exception()
    Traceback (most recent call last):
        ...
    ValueError: negative
    """
    return raises_explicitly(-1)


# --- assert in body ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int uses_assert(int x):
    assert x >= 0
    return x


def test_negative_assert():
    """Function with assert must NOT be inferred never_raises.

    >>> test_negative_assert()
    3
    """
    return uses_assert(3)


def test_negative_assert_raises():
    """assert with false condition raises AssertionError.

    >>> test_negative_assert_raises()
    Traceback (most recent call last):
        ...
    AssertionError
    """
    return uses_assert(-1)


# --- Python attribute access ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef object get_py_attr(object obj):
    return obj.__class__.__name__


def test_negative_py_attr():
    """Python attribute access can raise AttributeError → not safe.

    >>> test_negative_py_attr()
    'int'
    """
    return get_py_attr(42)


# --- variable divisor (could be zero) ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int variable_div(int a, int b):
    return a // b


def test_negative_variable_div():
    """Variable divisor: zerodivision_check present → not safe.

    >>> test_negative_variable_div()
    2
    """
    return variable_div(6, 3)


def test_negative_variable_div_zero():
    """Variable divisor can be zero at runtime.

    >>> test_negative_variable_div_zero()
    Traceback (most recent call last):
        ...
    ZeroDivisionError: integer division or modulo by zero
    """
    return variable_div(1, 0)


# --- overflowcheck(True) arithmetic ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
@cython.overflowcheck(True)
cpdef int overflow_checked(int a, int b):
    return a + b


def test_negative_overflow_check():
    """overflowcheck(True) arithmetic can raise OverflowError → not safe.

    >>> test_negative_overflow_check()
    5
    """
    return overflow_checked(2, 3)


# --- explicit except? -1 clause (has_explicit_exc_clause) ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int explicit_except(int x) except? -1:
    return x + 1


def test_negative_explicit_except():
    """Explicit except clause is user-specified: pass must not override it.

    >>> test_negative_explicit_except()
    6
    """
    return explicit_except(5)


# --- non-final class cpdef method with safe body ---
cdef class NonFinalWithSafeBody:
    cdef int _v

    def __init__(self, int v):
        self._v = v

    @cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
    cpdef int get_v(self):
        # Safe body, but non-final → vtable overrides possible → no tier-1 marking.
        return self._v


def test_negative_non_final_cpdef():
    """Non-final cpdef must NOT be tier-1 inferred even with a safe body.

    >>> test_negative_non_final_cpdef()
    42
    """
    cdef NonFinalWithSafeBody obj = NonFinalWithSafeBody(42)
    return obj.get_v()


# --- closure inside body ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int has_closure(int x):
    def inner():
        return x
    return inner()


def test_negative_closure():
    """Function with a closure must NOT be inferred never_raises.

    >>> test_negative_closure()
    7
    """
    return has_closure(7)


# --- generator function (not cpdef-compatible at all, but also not never_raises) ---
def is_generator(n):
    for i in range(n):
        yield i


def test_negative_generator():
    """Generator function must NOT be inferred never_raises.

    >>> test_negative_generator()
    [0, 1, 2]
    """
    return list(is_generator(3))


# --- object return that builds a tuple ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef object builds_tuple(int x, int y):
    return (x, y)


def test_negative_tuple_build():
    """Tuple construction allocates → can fail → not safe.

    >>> test_negative_tuple_build()
    (3, 4)
    """
    return builds_tuple(3, 4)


# --- C-to-Py coercion in body ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef object cint_to_py(int x):
    cdef object result = x   # C→Py integer boxing can fail
    return result


def test_negative_coerce_to_py():
    """C→Py coercion allocates a Python int → not safe.

    >>> test_negative_coerce_to_py()
    5
    """
    return cint_to_py(5)


# --- mutual recursion cycle (conservative: cycle → unsafe) ---
@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int cycle_a(int n):
    if n <= 0:
        return 0
    return cycle_b(n - 1)

@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
cpdef int cycle_b(int n):
    if n <= 0:
        return 0
    return cycle_a(n - 1)


def test_negative_mutual_recursion():
    """Mutually recursive functions form a cycle → conservative: not safe.

    >>> test_negative_mutual_recursion()
    0
    """
    return cycle_a(4)


# ===========================================================================
# RUNTIME SEMANTICS — all raising negatives propagate correctly
# ===========================================================================

def test_raising_functions_propagate():
    """All raising negative cases propagate exceptions at runtime.

    >>> test_raising_functions_propagate()
    'ok'
    """
    # raises_explicitly
    try:
        raises_explicitly(-1)
        assert False, "should have raised"
    except ValueError as e:
        assert "negative" in str(e), str(e)

    # uses_assert
    try:
        uses_assert(-1)
        assert False, "should have raised"
    except AssertionError:
        pass

    # variable_div
    try:
        variable_div(1, 0)
        assert False, "should have raised"
    except ZeroDivisionError:
        pass

    return 'ok'


# ===========================================================================
# RUNTIME SEMANTICS — Python subclass override of NON-final cpdef dispatches
# ===========================================================================

class PyChildNonFinal(NonFinalWithSafeBody):
    def get_v(self):
        return 999


def test_python_subclass_dispatch():
    """Python subclass override of non-final cpdef must be dispatched.

    >>> test_python_subclass_dispatch()
    999
    """
    # Statically typed as base: OverrideCheckNode dispatches to Python override.
    cdef NonFinalWithSafeBody obj = PyChildNonFinal(0)
    return obj.get_v()


# ===========================================================================
# OPT-OUT — @cython.infer_noexcept(False) on a safe body
# ===========================================================================

@cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
@cython.infer_noexcept(False)
cpdef int opted_out_safe(int x):
    # Body is provably safe, but directive disables inference for this function.
    return x + 1


def test_opt_out():
    """@cython.infer_noexcept(False) must suppress inference even for safe bodies.

    >>> test_opt_out()
    6
    """
    return opted_out_safe(5)


# ===========================================================================
# SPEC-INHERITANCE INTERACTION
# Non-final base with provably safe body + cdef subclass override that raises.
# Must compile WITHOUT "Exception specification is wider" error.
# The base is NOT tier-1 marked (non-final), so the override's spec inheritance
# works normally.  The raise from the override must propagate through a base-typed
# vtable call.
# ===========================================================================

cdef class SafeBase:
    cdef int _v

    def __init__(self, int v):
        self._v = v

    cpdef int get_v(self):
        # Safe body, non-final class → NOT tier-1 marked → spec stays intact for subclasses.
        return self._v


cdef class RaisingChild(SafeBase):
    # Unannotated override: inherits exception spec from SafeBase.get_v.
    # Because SafeBase.get_v was NOT infer-noexcept marked (non-final), the
    # inherited spec is unchanged and this override compiles cleanly even though
    # the body raises.
    cpdef int get_v(self):
        raise RuntimeError("child raises")


def test_spec_inheritance_safe_base_raising_child():
    """Base not marked noexcept → raising override compiles; raise propagates via vtable.

    >>> test_spec_inheritance_safe_base_raising_child()
    Traceback (most recent call last):
        ...
    RuntimeError: child raises
    """
    cdef SafeBase obj = RaisingChild(0)
    return obj.get_v()


def test_spec_inheritance_base_call_ok():
    """Direct base-typed call to SafeBase still works normally.

    >>> test_spec_inheritance_base_call_ok()
    10
    """
    cdef SafeBase obj = SafeBase(10)
    return obj.get_v()
