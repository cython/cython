# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef
from cython import cclass, int, final, public, no_ccall


@cclass
class Base:
    """Simplest base case"""

    def ret3(self) -> int:
        # This function is automatically promoted to cpdef
        return 3

@final
@cclass
class BaseFinal:
    """Final Class"""

    def ret2(self) -> int:
        # This function is automatically promoted to cpdef
        # being final, it can be optimized
        return 2


# Auto cpdef causes the fn() function becomes public, thus Vector needs to be public too.
@public
@cclass
class Vector:
    a: int
    b: int

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.a + other.a, self.b + other.b)

    def length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        return self.a*self.a + self.b*self.b

    def __eq__(self, other: 'Vector') -> bool:
        return self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return f"Vector({self.a}, {self.b})"


def fn() -> Vector:
    a: int = BaseFinal().ret2()  # optimized direct C-call of promoted to cpdef
    b: int = Base().ret3()  # optimized vtable-call of promoted cpdef
    return Vector(a, b)


def test_vector(v):
    """
    Just test a simple class with auto_cpdef enabled.

    >>> Base().ret3()
    3
    >>> test_vector(Vector(2, 3) + Vector(4, 5))
    Vector(6, 8)
    >>> test_vector(fn().length_sq())
    13
    >>> test_vector(Vector(2, 3) == Vector(4, 5))  # special method semantics preserved
    False
    >>> test_vector(Vector(2, 3) == Vector(2, 3))
    True
    >>> test_vector(Vector(2, 3).__eq__(Vector(4, 5)))  # special method semantics preserved
    False
    >>> test_vector(Vector(2, 3).__eq__(Vector(2, 3)))
    True
    """
    return v


@public
@final
@cclass
class VectorFinal(Vector):

    def length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        return 23

    def origin_length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        # accessing base class through super() is optimized too
        return super().length_sq()

    @no_ccall
    def origin_length_sq_no_ccall(self) -> int:
        # This function is PREVENTED to become cpdef
        return super().length_sq() + 1


def fn2() -> VectorFinal:
    return VectorFinal(2, 3)


def test_vector_final(v):
    """
    Just test a simple final class with auto_cpdef enabled.

    >>> test_vector(VectorFinal(2, 3) + VectorFinal(4, 5))
    Vector(6, 8)
    >>> test_vector(VectorFinal(2, 3).length_sq())
    23
    >>> test_vector(fn2().origin_length_sq())
    13
    >>> test_vector(fn2().origin_length_sq_no_ccall())
    14
    """
    return v


@cclass
class RefBase:
    def make_value(self) -> int:
        # promoted to cpdef; referenced below as a *value* (callback), not called
        return 7


@cclass
class RefSub(RefBase):
    pass


def use_inherited_method_ref():
    """
    A cpdef method referenced as a value (here an *inherited* one) must resolve
    to the bound Python method, not the raw vtable function pointer. Regression
    test: inherited cmethod entries have no `as_variable`, which previously sent
    this through a `to_py` of the vtable pointer whose signature includes
    `__pyx_skip_dispatch` -- a C compile error ('no matching function').

    >>> cb = use_inherited_method_ref()
    >>> cb()
    7
    >>> callable(cb)
    True
    """
    sub: RefSub = RefSub()
    callback = sub.make_value   # inherited cpdef method taken as a value
    return callback


@cclass
class IThing:
    @property
    def total(self) -> int:
        raise NotImplementedError()

    @property
    def items(self) -> object:
        raise NotImplementedError()


@cclass
class Thing(IThing):
    _values: list

    def __init__(self, values) -> None:
        self._values = list(values)

    @property
    def total(self) -> int:
        # closure (generator EXPRESSION) -- not a generator getter; must still
        # become a cproperty C getter and fill the inherited vtable slot.
        return sum(v for v in self._values)

    @property
    def items(self) -> object:
        # generator getter (`yield`) -- cannot be a C getter; stays a Python
        # getter and must NOT crash.
        for v in self._values:
            yield v


def use_closure_property_override():
    """
    A closure (genexpr) property getter overriding an abstract cproperty must
    fill the vtable slot, so a statically-typed *base* access dispatches to the
    override -- not the abstract base getter (which would raise NotImplementedError,
    swallowed as "Exception ignored in: 'IThing.total.__get__'").

    >>> use_closure_property_override()
    6
    """
    base: IThing = Thing([1, 2, 3])
    return base.total   # typed-base access -> vtable dispatch -> Thing.total


def use_generator_property_getter():
    """
    A generator property getter (`yield`) stays a Python getter and must work
    (it cannot be a plain C getter; converting one used to crash).

    >>> list(use_generator_property_getter())
    [1, 2, 3]
    """
    t: Thing = Thing([1, 2, 3])
    return t.items


# --- Trampoline: a def override that cannot itself be promoted to cpdef -------
# (a closure or generator) still fills the inherited vtable slot via a synthesised
# C trampoline, so base-typed / super() dispatch resolves to the override.

@cclass
class TBase:
    def make(self, x: int) -> int:
        # promoted to cpdef -> has a vtable slot
        return x + 1

    def stream(self, n: int) -> object:
        # promoted to cpdef
        return list(range(n))


@cclass
class TClosure(TBase):
    def make(self, x: int) -> int:
        # closure -> NOT cdef-func-compatible -> trampoline fills the slot
        def inner():
            return x * 10
        return inner() + super().make(x)


@cclass
class TGen(TBase):
    def stream(self, n: int) -> object:
        # generator -> NOT cdef-func-compatible -> trampoline fills the slot
        for i in range(n):
            yield i * 2


@cclass
class TDispatcher:
    @no_ccall
    def via_base_make(self, b: TBase, x: int) -> int:
        # statically base-typed receiver -> C vtable dispatch must reach the
        # override's trampoline.
        return b.make(x)


def _dispatch_make(b, x):
    return TDispatcher().via_base_make(b, x)


def test_method_trampoline():
    """
    >>> TBase().make(5)
    6
    >>> TClosure().make(5)            # 50 (closure) + 6 (super) == 56
    56
    >>> _dispatch_make(TBase(), 5)    # vtable -> TBase.make
    6
    >>> _dispatch_make(TClosure(), 5) # vtable -> TClosure trampoline -> override
    56
    >>> list(TBase().stream(3))
    [0, 1, 2]
    >>> list(TGen().stream(3))        # generator override via trampoline
    [0, 2, 4]
    >>> b = TBase()
    >>> list(_dispatch_stream(TGen(), 3))   # base-typed -> TGen trampoline
    [0, 2, 4]
    """


@cclass
class TStreamDispatcher:
    @no_ccall
    def via_base_stream(self, b: TBase, n: int) -> object:
        return b.stream(n)


def _dispatch_stream(b, n):
    return TStreamDispatcher().via_base_stream(b, n)


def test_python_override_through_trampoline():
    """
    A pure-Python subclass overriding a trampolined method must still be reached
    through C (vtable) dispatch -- the trampoline carries the same OverrideCheck
    as a normal cpdef method.

    >>> class PyClosure(TClosure):
    ...     def make(self, x):
    ...         return 1000
    >>> _dispatch_make(PyClosure(), 5)
    1000
    """
