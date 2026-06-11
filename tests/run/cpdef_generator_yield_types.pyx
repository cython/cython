# cython: annotation_typing=True, language_level=3
# mode: run
# tag: generator,yield,typing,annotation_typing

"""
Compile-time yield-type checking: verify that annotated generators compile and run
correctly, and that no false positives are raised for compatible types.
"""

import cython
from typing import Iterator, Iterable, Generator
try:
    from collections.abc import Iterator as AbcIterator, Iterable as AbcIterable
except ImportError:
    # Python < 3.3 compat (unlikely in practice)
    from collections import Iterator as AbcIterator, Iterable as AbcIterable


# --- typing.Iterator ---

def gen_int_iterator() -> Iterator[int]:
    """
    >>> list(gen_int_iterator())
    [1, 2, 3]
    """
    yield 1
    yield 2
    yield 3


def gen_c_int_iterator() -> Iterator[int]:
    """
    >>> list(gen_c_int_iterator())
    [10, 20]
    """
    n: cython.int = 10
    yield n
    n = 20
    yield n


def gen_float_iterator() -> Iterator[float]:
    """
    >>> list(gen_float_iterator())
    [1.5, 2.5]
    """
    yield 1.5
    yield 2.5


def gen_int_where_float_declared() -> Iterator[float]:
    """Yielding int where float declared is allowed (numeric widening).
    >>> list(gen_int_where_float_declared())
    [1, 2]
    """
    yield 1
    yield 2


def gen_bool_where_int_declared() -> Iterator[int]:
    """bool is a subtype of int — allowed.
    >>> list(gen_bool_where_int_declared())
    [True, False]
    """
    yield True
    yield False


# --- typing.Iterable ---

def gen_iterable() -> Iterable[int]:
    """
    >>> list(gen_iterable())
    [10, 20]
    """
    yield 10
    yield 20


# --- typing.Generator[YieldType, SendType, ReturnType] ---

def gen_generator_form() -> Generator[int, None, None]:
    """
    >>> list(gen_generator_form())
    [42, 43]
    """
    yield 42
    yield 43


# --- collections.abc forms ---

def gen_abc_iterator() -> AbcIterator[int]:
    """
    >>> list(gen_abc_iterator())
    [100, 200]
    """
    yield 100
    yield 200


def gen_abc_iterable() -> AbcIterable[int]:
    """
    >>> list(gen_abc_iterable())
    [5, 6]
    """
    yield 5
    yield 6


# --- typing attribute form (import typing; typing.Iterator[...]) ---
import typing

def gen_typing_attr() -> typing.Iterator[int]:
    """
    >>> list(gen_typing_attr())
    [7, 8]
    """
    yield 7
    yield 8


# --- yield from with compatible types ---

def _source_int() -> Iterator[int]:
    yield 1
    yield 2

def gen_yield_from_int() -> Iterator[int]:
    """yield from same-typed source is allowed.
    >>> list(gen_yield_from_int())
    [1, 2]
    """
    yield from _source_int()


def _source_bool() -> Iterator[bool]:
    yield True
    yield False

def gen_yield_from_bool_where_int() -> Iterator[int]:
    """bool extends int — delegating is allowed.
    >>> list(gen_yield_from_bool_where_int())
    [True, False]
    """
    yield from _source_bool()


# --- yield from untyped generator (no check — no false positives) ---

def _untyped_source():
    yield "anything"

def gen_yield_from_untyped() -> Iterator[int]:
    """Delegating to an unannotated generator: no check, no error.
    >>> list(gen_yield_from_untyped())
    ['anything']
    """
    yield from _untyped_source()


# --- yield from untyped list (no check) ---

def gen_yield_from_list() -> Iterator[int]:
    """Generic list — no check, no error.
    >>> list(gen_yield_from_list())
    [1, 2, 3]
    """
    yield from [1, 2, 3]


# --- Unannotated yields — no false positives ---

def gen_no_annotation():
    """Unannotated generator: no check at all.
    >>> list(gen_no_annotation())
    ['a', 1, 2.0]
    """
    yield 'a'
    yield 1
    yield 2.0


# --- Non-generator with -> Iterator[int] annotation (no check) ---

def non_gen_annotated() -> Iterator[int]:
    """Non-generator function with Iterator annotation: completely unchanged.
    >>> non_gen_annotated()
    42
    """
    return 42


# --- Unknown name Iterator (not imported) — no check ---

def gen_unknown_annotation() -> 'Iterator[int]':
    """String annotation — no check.
    >>> list(gen_unknown_annotation())
    ['x']
    """
    yield 'x'


# --- @ccall promoted generator with correct type annotation ---

@cython.ccall
def ccall_gen_typed() -> Iterator[int]:
    """Promoted generator with a correct annotation compiles and runs.
    >>> list(ccall_gen_typed())
    [10, 20]
    """
    n: cython.int = 10
    yield n
    yield 2 * n


@cython.ccall
def ccall_gen_chain() -> Iterator[int]:
    """yield from between two promoted, annotated generators (compatible).
    Exercises declared_yield_type resolution through the cfunction entry.
    >>> list(ccall_gen_chain())
    [10, 20, 7]
    """
    yield from ccall_gen_typed()
    i: cython.int = 7
    yield i


@cython.ccall
def call_ccall_gen_chain():
    """C-call into the promoted annotated generator from another ccall function.
    >>> call_ccall_gen_chain()
    [10, 20, 7]
    """
    return list(ccall_gen_chain())


# --- cclass generator method with correct type annotation ---

cdef class TypedBox:
    """Generator method with @ccall + annotation gets a vtable slot and
    its yields are type-checked (all compatible here).

    >>> box = TypedBox(3)
    >>> list(box.items())
    [0, 1, 2]
    >>> box.total()
    3
    """
    cdef int n

    def __init__(self, n):
        self.n = n

    @cython.ccall
    def items(self) -> Iterator[int]:
        i: cython.int
        for i in range(self.n):
            yield i

    @cython.ccall
    def total(self) -> cython.int:
        t: cython.int = 0
        for v in self.items():
            t += v
        return t
