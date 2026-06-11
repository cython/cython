# cython: annotation_typing=True, language_level=3
# mode: error

"""
Compile-time yield-type checking: verify that definite mismatches produce errors.
"""

from typing import Iterator, Iterable, Generator
from collections.abc import Iterable as AbcIterable

# --- typing.Iterator: definite mismatches ---

def gen_int_yields_str() -> Iterator[int]:
    yield "abc"       # ERROR: str where int declared


def gen_int_yields_bytes() -> Iterator[int]:
    b: bytes = b"x"
    yield b           # ERROR: bytes where int declared


# --- Generator[int, None, None] form ---

def gen_generator_form_bad() -> Generator[int, None, None]:
    yield b"bytes"    # ERROR: bytes where int declared


# --- collections.abc.Iterable ---

def gen_abc_iterable_bad() -> AbcIterable[int]:
    yield "str_val"   # ERROR: str where int declared


# --- float declared, string yields error ---

def gen_float_yields_str() -> Iterator[float]:
    yield "s"         # ERROR: str where float declared


# --- yield from: delegation to incompatible annotated generator ---

def _str_source() -> Iterator[str]:
    yield "a"

def gen_int_yields_from_str() -> Iterator[int]:
    yield from _str_source()    # ERROR: str source where int declared


# --- yield from bytes where str declared ---

def gen_str_yields_from_bytes() -> Iterator[str]:
    b: bytes = b"abc"
    yield from b            # ERROR: bytes yields int items, not str


_ERRORS = """
14:10: Generator declared as yielding 'int' cannot yield a value of type 'str object'
19:10: Generator declared as yielding 'int' cannot yield a value of type 'bytes object'
25:10: Generator declared as yielding 'int' cannot yield a value of type 'bytes object'
31:10: Generator declared as yielding 'int' cannot yield a value of type 'str object'
37:10: Generator declared as yielding 'float' cannot yield a value of type 'str object'
46:26: Generator declared as yielding 'int' cannot delegate to a generator yielding 'str object'
53:15: Generator declared as yielding 'str object' cannot delegate to a generator yielding 'int object'
"""
