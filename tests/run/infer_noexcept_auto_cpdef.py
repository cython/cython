# cython: auto_cpdef=True
# cython: language_level=3
# mode: run
# tag: infer_noexcept, auto_cpdef, optimization

"""Tests for InferNoexcept combined with auto_cpdef=True in pure-Python syntax.

Covers:
- Final cclass with C-annotated attrs, ccall methods: C-typed ccall (tier 1, never_raises)
  and object-forwarding ccall (tier 1, never_raises flag suppresses NULL check).
- Tuple-constructing ccall: negative (tuple alloc can fail).
- super().__init__ chain: final subclass -> non-final base (tier 2 via wrapper_call).
- Constructor call P(1, 2): exercising the ctor-optimizer per-call-site patch.

Note: @property accessors are deliberately avoided on @cython.final classes here
because auto_cpdef mode makes property getter functions CYTHON_INLINE, and on
Darwin, CYTHON_INLINE without static causes missing-symbol linker errors when the
function address is stored in a vtable.  The property-getter inference path is
already exercised by tests/run/infer_noexcept.pyx.
"""

import cython


# ===========================================================================
# Final class — C-typed attrs, ccall methods
# ===========================================================================

@cython.final
@cython.cclass
class Point2D:
    _x: cython.int
    _y: cython.int
    _label: object  # PyObject field

    def __init__(self, x: cython.int, y: cython.int, label=None):
        self._x = x
        self._y = y
        self._label = label

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    @cython.ccall
    def get_x(self) -> cython.int:
        return self._x

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    @cython.ccall
    def get_label(self) -> object:
        # Object-forwarding ccall: never_raises flag suppresses NULL-check at caller.
        return self._label

    @cython.test_assert_path_exists("//CFuncDefNode[@type.never_raises = True]")
    @cython.ccall
    def norm2(self) -> cython.double:
        return self._x * self._x + self._y * self._y

    @cython.test_fail_if_path_exists("//CFuncDefNode[@type.never_raises = True]")
    @cython.ccall
    def make_tuple(self) -> object:
        return (self._x, self._y)


# Callers that let us assert SimpleCallNode[@function.type.never_raises = True]
# for the object-forwarding ccall (which uses the never_raises flag, not
# exception_check clearing, to suppress the NULL check).

@cython.test_assert_path_exists(
    "//SimpleCallNode[@function.type.never_raises = True]",
)
def caller_get_label(p: Point2D) -> object:
    """Caller for object-forwarding ccall: SimpleCallNode should have never_raises flag.

    >>> p = Point2D(1, 2, 'hi')
    >>> caller_get_label(p)
    'hi'
    """
    return p.get_label()


def test_ctyped_getter():
    """C-typed ccall getter works correctly.

    >>> test_ctyped_getter()
    7
    """
    p = Point2D(7, 3)
    return p.get_x()


def test_object_getter():
    """Object-forwarding ccall getter returns the stored object.

    >>> test_object_getter()
    'hello'
    """
    p = Point2D(1, 2, 'hello')
    return p.get_label()


def test_tuple_getter():
    """Tuple-constructing ccall still works correctly at runtime.

    >>> test_tuple_getter()
    (3, 4)
    """
    p = Point2D(3, 4)
    return p.make_tuple()


def test_norm2():
    """C arithmetic ccall method: inferred never_raises, correct value.

    >>> test_norm2() in (25, 25.0)
    True
    """
    p = Point2D(3, 4)
    return p.norm2()


# ===========================================================================
# super().__init__ chain — tier-2 wrapper_call per-call-site
# ===========================================================================

@cython.cclass
class BaseWithInit:
    """Non-final base class with a simple field-assigning __init__ (tier-2 eligible)."""
    _val: cython.int

    def __init__(self, val: cython.int):
        self._val = val

    @cython.ccall
    def val(self) -> cython.int:
        return self._val


@cython.final
@cython.cclass
class DerivedFinal(BaseWithInit):
    """Final subclass: super().__init__ is a direct call (wrapper_call=True -> tier 2)."""
    _extra: cython.int

    def __init__(self, val: cython.int, extra: cython.int):
        super().__init__(val)
        self._extra = extra

    @cython.ccall
    def extra(self) -> cython.int:
        return self._extra

    @cython.ccall
    def total(self) -> cython.int:
        return self._val + self._extra


def test_super_init_chain():
    """super().__init__ chain: fields initialized correctly, values are correct.

    >>> test_super_init_chain()
    (10, 5, 15)
    """
    d = DerivedFinal(10, 5)
    return (d.val(), d.extra(), d.total())


# ===========================================================================
# Constructor call exercising ctor-optimizer per-call-site noexcept patch
# ===========================================================================

@cython.cclass
class Pair:
    """Simple non-final class for constructor-optimizer tests."""
    _a: cython.int
    _b: cython.int

    def __init__(self, a: cython.int, b: cython.int):
        self._a = a
        self._b = b

    @cython.ccall
    def a(self) -> cython.int:
        return self._a

    @cython.ccall
    def b(self) -> cython.int:
        return self._b

    @cython.ccall
    def sum(self) -> cython.int:
        return self._a + self._b


def test_ctor_call_simple():
    """Constructor call Pair(1, 2): ctor-optimizer produces direct tp_new + __init__ call.

    >>> test_ctor_call_simple()
    (1, 2, 3)
    """
    p = Pair(1, 2)
    return (p.a(), p.b(), p.sum())


def test_ctor_call_expression_context():
    """Constructor call in an expression context.

    >>> test_ctor_call_expression_context()
    10
    """
    return Pair(3, 7).sum()


def test_ctor_call_multiple():
    """Multiple constructor calls in the same function.

    >>> test_ctor_call_multiple()
    (3, 7)
    """
    p1 = Pair(1, 2)
    p2 = Pair(3, 4)
    return (p1.sum(), p2.sum())


# ===========================================================================
# Runtime: exceptions still propagate through non-final non-inferred methods
# ===========================================================================

@cython.cclass
class WithRaisingMethod:
    _x: cython.int

    def __init__(self, x: cython.int):
        self._x = x

    @cython.ccall
    def compute(self) -> cython.int:
        if self._x < 0:
            raise ValueError("negative input: %d" % self._x)
        return self._x * 2


def test_raising_method_propagates():
    """Raising ccall method: exception must propagate.

    >>> test_raising_method_propagates()
    10
    """
    obj = WithRaisingMethod(5)
    return obj.compute()


def test_raising_method_exception():
    """Raising ccall method raises correctly on bad input.

    >>> test_raising_method_exception()
    Traceback (most recent call last):
        ...
    ValueError: negative input: -1
    """
    obj = WithRaisingMethod(-1)
    return obj.compute()
