# cython: auto_cpdef=True
# cython: language_level=3
# mode: run
# tag: generators, cpdef, cclass

"""
Tests for cclass generator methods promoted to cpdef via auto_cpdef.

Each @cython.cclass generator def gets a fresh vtable slot (via a C trampoline
that forwards to the generator's __pyx_pf_ body). Derived classes that override
a base's generator method share the same inherited slot (so base-typed dispatch
works correctly).
"""

import cython
from typing import Iterator


# ---------------------------------------------------------------------------
# 1. Basic fresh-slot trampoline
# ---------------------------------------------------------------------------

@cython.cclass
class Base:
    """Generator method items() gets a fresh vtable slot.

    >>> b = Base()
    >>> list(b.items())
    [1, 2]
    >>> b.call_items()
    [1, 2]
    """

    def items(self):
        yield 1
        yield 2

    def call_items(self):
        """C dispatch through vtable (skip_dispatch=1 path)."""
        return list(self.items())


# ---------------------------------------------------------------------------
# 2. Typed args + typed locals inside the generator
# ---------------------------------------------------------------------------

@cython.cclass
class TypedArgs:
    """Generator with typed args and locals.

    >>> t = TypedArgs(10)
    >>> list(t.range_items(3))
    [10, 11, 12]
    """

    value: cython.int

    def __init__(self, value: cython.int):
        self.value = value

    def range_items(self, count: cython.int):
        i: cython.int
        for i in range(count):
            yield self.value + i


# ---------------------------------------------------------------------------
# 3. Generator method WITH defaults
# ---------------------------------------------------------------------------

@cython.cclass
class WithDefaults:
    """Generator with default argument.

    >>> w = WithDefaults()
    >>> list(w.items())
    [0, 1, 2]
    >>> list(w.items(5))
    [5, 6, 7]
    """

    def items(self, start: cython.int = 0):
        yield start
        yield start + 1
        yield start + 2


# ---------------------------------------------------------------------------
# 4. Non-generator cpdef calling self.generator_method() — C dispatch
# ---------------------------------------------------------------------------

@cython.cclass
class WithCMethod:
    """Non-generator cpdef method calling generator via C dispatch.

    >>> obj = WithCMethod()
    >>> obj.collect()
    [10, 20, 30]
    """

    def values(self):
        yield 10
        yield 20
        yield 30

    def collect(self) -> list:
        """This becomes a cpdef method that dispatches to self.values() via vtable."""
        return list(self.values())


# ---------------------------------------------------------------------------
# 5. Inheritance: Derived overrides generator, base-typed dispatch hits override
# ---------------------------------------------------------------------------

@cython.cclass
class InheritBase:
    """
    >>> b = InheritBase()
    >>> list(b.items())
    [1, 2]
    """

    def items(self):
        yield 1
        yield 2


@cython.cclass
class InheritDerived(InheritBase):
    """Override hits derived generator via vtable.

    >>> d = InheritDerived()
    >>> list(d.items())
    [3, 4]
    """

    def items(self):
        yield 3
        yield 4


def dispatch_base_typed_ref():
    """Base-typed variable dispatches to Derived override.

    >>> dispatch_base_typed_ref()
    [3, 4]
    """
    b: InheritBase = InheritDerived()
    return list(b.items())


# ---------------------------------------------------------------------------
# 6. Pure-Python subclass overriding generator — OverrideCheckNode fires
# ---------------------------------------------------------------------------

@cython.cclass
class ForPySubclass:
    """
    >>> o = ForPySubclass()
    >>> list(o.items())
    [1, 2]
    """

    def items(self):
        yield 1
        yield 2


class PythonSub(ForPySubclass):
    """Pure-Python subclass overrides items.

    >>> p = PythonSub()
    >>> list(p.items())
    [100, 200]
    """

    def items(self):
        yield 100
        yield 200


def dispatch_py_sub_via_base():
    """Python subclass override is reached through base-typed dispatch.

    >>> dispatch_py_sub_via_base()
    [100, 200]
    """
    b: ForPySubclass = PythonSub()
    return list(b.items())


# ---------------------------------------------------------------------------
# 7. cclass whose ONLY method is a generator (vtable-allocation edge case)
# ---------------------------------------------------------------------------

@cython.cclass
class OnlyGenerator:
    """A cclass whose only method is a generator — vtable must be allocated.

    >>> o = OnlyGenerator()
    >>> list(o.single())
    [42]
    """

    def single(self):
        yield 42


# ---------------------------------------------------------------------------
# 8. Base cpdef non-generator overridden in subclass by a generator
#    → inherited-slot trampoline (existing path, no new slot)
# ---------------------------------------------------------------------------

@cython.cclass
class NonGenBase:
    """
    >>> b = NonGenBase()
    >>> list(b.items())
    [10, 20]
    """

    def items(self):
        """Return an iterable — compatible with a generator override."""
        return iter([10, 20])


@cython.cclass
class GenOverride(NonGenBase):
    """Generator overriding a promoted non-generator cpdef — inherited slot trampoline.

    >>> d = GenOverride()
    >>> list(d.items())
    [30, 40]
    """

    def items(self):
        yield 30
        yield 40


def dispatch_gen_override():
    """Base-typed dispatch hits GenOverride.items generator.

    >>> dispatch_gen_override()
    [30, 40]
    """
    b: NonGenBase = GenOverride()
    return list(b.items())


# ---------------------------------------------------------------------------
# 9. super().items() from Derived — correct behavior (may or may not optimize)
# ---------------------------------------------------------------------------

@cython.cclass
class SuperBase:
    """
    >>> b = SuperBase()
    >>> list(b.items())
    [1]
    """

    def items(self):
        yield 1


@cython.cclass
class SuperDerived(SuperBase):
    """Derived generator calling super().items().

    >>> d = SuperDerived()
    >>> list(d.items())
    [2, 1]
    """

    def items(self):
        yield 2
        for x in super().items():
            yield x


# ---------------------------------------------------------------------------
# 10. Annotated generator method (auto-promoted, fresh slot) — correct typing
# ---------------------------------------------------------------------------

@cython.cclass
class AnnotatedBox:
    """Auto-promoted generator method with a yield-type annotation.

    >>> box = AnnotatedBox(3)
    >>> list(box.items())
    [0, 1, 2]
    >>> box.total()
    3
    """
    n: cython.int

    def __init__(self, n: cython.int):
        self.n = n

    def items(self) -> Iterator[int]:
        i: cython.int
        for i in range(self.n):
            yield i

    def chained(self) -> Iterator[int]:
        """yield from the promoted annotated sibling method (compatible).

        >>> list(AnnotatedBox(2).chained())
        [0, 1, -1]
        """
        yield from self.items()
        yield -1

    def total(self) -> cython.int:
        t: cython.int = 0
        for v in self.items():
            t += v
        return t


# ---------------------------------------------------------------------------
# 11. Exceptions raised inside promoted generator methods (depth 1 and 2)
# ---------------------------------------------------------------------------

@cython.cclass
class RaisingBox:
    """Generator methods whose bodies raise, dispatched through vtable slots.

    Depth 1 — the body raises after its yields:
    >>> g = RaisingBox().items(2)
    >>> next(g), next(g)
    (0, 1)
    >>> next(g)
    Traceback (most recent call last):
    ...
    RuntimeError: box exhausted at 2

    Depth 2 — a generator method delegating to a sibling generator method via
    self (vtable dispatch) propagates the inner exception through both frames:
    >>> g = RaisingBox().nested(1)
    >>> next(g)
    0
    >>> next(g)
    Traceback (most recent call last):
    ...
    RuntimeError: box exhausted at 1
    """

    def items(self, n: cython.int):
        i: cython.int
        for i in range(n):
            yield i
        raise RuntimeError("box exhausted at %d" % n)

    def nested(self, n: cython.int):
        yield from self.items(n)

    def consume(self, n: cython.int):
        """Promoted (non-generator) cpdef method consuming the two-level chain
        through C dispatch; the exception must surface intact.

        >>> RaisingBox().consume(3)
        ('caught', 'box exhausted at 3', [0, 1, 2])
        """
        out = []
        try:
            for v in self.nested(n):
                out.append(v)
        except RuntimeError as exc:
            return ('caught', str(exc), out)


@cython.cclass
class RaisingDerived(RaisingBox):
    """Cross-class depth-2: the derived generator delegates to the BASE class's
    raising generator through super().

    >>> g = RaisingDerived().nested(1)
    >>> next(g), next(g)
    (-1, 0)
    >>> next(g)
    Traceback (most recent call last):
    ...
    RuntimeError: box exhausted at 1
    """

    def nested(self, n: cython.int):
        yield -1
        yield from super().nested(n)


def consume_raising_base_typed(n: cython.int):
    """Base-typed C dispatch into the override; inner base exception propagates
    through three generator frames (derived.nested -> base.nested -> base.items).

    >>> consume_raising_base_typed(2)
    ('caught', 'box exhausted at 2', [-1, 0, 1])
    """
    box: RaisingBox = RaisingDerived()
    out = []
    try:
        for v in box.nested(n):
            out.append(v)
    except RuntimeError as exc:
        return ('caught', str(exc), out)
