# cython: auto_cpdef=True
# cython: language_level=3
# mode: run
# tag: auto_cpdef

"""Tests for auto_cpdef promotion of methods with optional arguments, and for
the constructor / super() optimizations that route those calls through the C
calling convention without boxing typed arguments.
"""

import cython


# ---------------------------------------------------------------------------
# Basic constructor with optional Python-object arguments
# ---------------------------------------------------------------------------

@cython.cclass
class PyOptBase:
    x: object
    y: object
    z: object

    def __init__(self, x, y=10, z=None):
        self.x = x
        self.y = y
        self.z = z

    def values(self):
        return (self.x, self.y, self.z)


def test_pyopt_ctor_required_only():
    """
    >>> test_pyopt_ctor_required_only()
    ('a', 10, None)
    """
    obj = PyOptBase('a')
    return obj.values()


def test_pyopt_ctor_one_optional():
    """
    >>> test_pyopt_ctor_one_optional()
    ('a', 20, None)
    """
    obj = PyOptBase('a', 20)
    return obj.values()


def test_pyopt_ctor_all_optional():
    """
    >>> test_pyopt_ctor_all_optional()
    ('a', 20, 'z')
    """
    obj = PyOptBase('a', 20, 'z')
    return obj.values()


# ---------------------------------------------------------------------------
# Constructor with typed (C-native) arguments — no PyObject boxing on the
# optimized call path.
# ---------------------------------------------------------------------------

@cython.cclass
class TypedOptBase:
    x: cython.int
    y: cython.double

    def __init__(self, x: cython.int, y: cython.double = 0.5):
        self.x = x
        self.y = y

    def values(self):
        return (self.x, self.y)


def test_typed_ctor_required_only():
    """
    >>> test_typed_ctor_required_only()
    (7, 0.5)
    """
    obj = TypedOptBase(7)
    return obj.values()


def test_typed_ctor_with_optional():
    """
    >>> test_typed_ctor_with_optional()
    (7, 3.14)
    """
    obj = TypedOptBase(7, 3.14)
    return obj.values()


# ---------------------------------------------------------------------------
# Regular methods with optional args
# ---------------------------------------------------------------------------

@cython.cclass
class MethodOpt:
    def greet(self, name, greeting="Hello", punct="!"):
        return "%s, %s%s" % (greeting, name, punct)


def test_method_opt_required_only():
    """
    >>> test_method_opt_required_only()
    'Hello, world!'
    """
    obj = MethodOpt()
    return obj.greet("world")


def test_method_opt_one_optional():
    """
    >>> test_method_opt_one_optional()
    'Hi, world!'
    """
    obj = MethodOpt()
    return obj.greet("world", "Hi")


def test_method_opt_all_optional():
    """
    >>> test_method_opt_all_optional()
    'Hey, world.'
    """
    obj = MethodOpt()
    return obj.greet("world", "Hey", ".")


# ---------------------------------------------------------------------------
# super().__init__() with optional args — same module
# ---------------------------------------------------------------------------

@cython.cclass
class DerivedOpt(PyOptBase):
    extra: object

    def __init__(self, x, y=10, z=None, extra=None):
        super().__init__(x, y, z)
        self.extra = extra

    def values(self):
        return (self.x, self.y, self.z, self.extra)


def test_derived_ctor_required_only():
    """
    >>> test_derived_ctor_required_only()
    ('b', 10, None, None)
    """
    obj = DerivedOpt('b')
    return obj.values()


def test_derived_ctor_with_optionals():
    """
    >>> test_derived_ctor_with_optionals()
    ('b', 30, 'zz', 'ex')
    """
    obj = DerivedOpt('b', 30, 'zz', 'ex')
    return obj.values()


def test_super_init_required_only():
    """Test super().__init__ passes required-only args (no optional).
    >>> test_super_init_required_only()
    ('c', 10, None, None)
    """
    obj = DerivedOpt('c')
    return obj.values()


def test_super_init_with_one_optional():
    """Test super().__init__ with one optional arg forwarded.
    >>> test_super_init_with_one_optional()
    ('c', 99, None, None)
    """
    obj = DerivedOpt('c', 99)
    return obj.values()


# ---------------------------------------------------------------------------
# super().method() with optional args — same module
# ---------------------------------------------------------------------------

@cython.cclass
class SuperMethodBase:
    def compute(self, a, b=100):
        return a + b


@cython.cclass
class SuperMethodDerived(SuperMethodBase):
    def compute_no_opt(self, a):
        # Call super without forwarding the optional arg → base uses b=100
        return super().compute(a) * 2

    def compute_with_opt(self, a, b=0):
        # Call super, explicitly passing the optional arg
        return super().compute(a, b) * 2


def test_super_method_required_only():
    """super().compute(a) with no optional → base uses b=100: 5+100=105, *2=210
    >>> test_super_method_required_only()
    210
    """
    obj = SuperMethodDerived()
    return obj.compute_no_opt(5)


def test_super_method_with_optional():
    """super().compute(a, b=3) passes b=3 to base → 5+3=8, *2=16
    >>> test_super_method_with_optional()
    16
    """
    obj = SuperMethodDerived()
    return obj.compute_with_opt(5, 3)


# ---------------------------------------------------------------------------
# Typed method with optional args — no boxing check via doctest behavior
# ---------------------------------------------------------------------------

@cython.cclass
class TypedMethod:
    def scale(self, x: cython.int, factor: cython.double = 2.0) -> cython.double:
        return x * factor


def test_typed_method_default():
    """
    >>> test_typed_method_default()
    10.0
    """
    obj = TypedMethod()
    return obj.scale(5)


def test_typed_method_explicit():
    """
    >>> test_typed_method_explicit()
    15.0
    """
    obj = TypedMethod()
    return obj.scale(5, 3.0)


# ---------------------------------------------------------------------------
# Self-referential constructor assignment: `v = T(... v.field ...)`.
# The statement-level constructor split must NOT fire here, because it would
# rebind `v` to the freshly-allocated (zeroed) object before evaluating the
# arguments that read `v.field`.  The expression-level path (temp) is correct.
# Regression for crop-chronicles `measure = Size(min(measure.width, ...), ...)`.
# ---------------------------------------------------------------------------

@cython.cclass
class Size2D:
    width: cython.int
    height: cython.int

    def __init__(self, width: cython.int, height: cython.int):
        self.width = width
        self.height = height


def test_self_referential_ctor():
    """
    >>> test_self_referential_ctor()
    (84, 88)
    """
    measure = Size2D(84, 88)
    min_w, max_w = 0, 1073741823
    min_h, max_h = 0, 1073741823
    measure = Size2D(
        max(min_w, min(measure.width, max_w)),
        max(min_h, min(measure.height, max_h)),
    )
    return (measure.width, measure.height)


def test_self_referential_ctor_swap():
    """
    >>> test_self_referential_ctor_swap()
    (88, 84)
    """
    measure = Size2D(84, 88)
    # Read both fields of the old object while building the new one.
    measure = Size2D(measure.height, measure.width)
    return (measure.width, measure.height)
