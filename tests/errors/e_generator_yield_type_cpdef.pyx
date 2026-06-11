# cython: annotation_typing=True, auto_cpdef=True, language_level=3
# mode: error

"""
Yield-type checking must also fire for generators that are PROMOTED to
cpdef/ccall (auto_cpdef module functions, @cython.ccall, and cclass generator
methods with fresh vtable slots).
"""

import cython
from typing import Iterator


# --- auto_cpdef-promoted module-level generator ---

def promoted_gen_bad() -> Iterator[int]:
    yield "abc"       # ERROR: str where int declared


# --- explicit @ccall generator ---

@cython.ccall
def ccall_gen_bad() -> Iterator[int]:
    b: bytes = b"x"
    yield b           # ERROR: bytes where int declared


# --- cclass generator method (fresh vtable slot) ---

cdef class Box:
    def items_bad(self) -> Iterator[int]:
        yield "nope"  # ERROR: str where int declared


# --- yield from between two PROMOTED generators with incompatible item types.
# This exercises declared_yield_type resolution through the swapped module
# entry (cfunction entry -> as_variable -> pydef entry). ---

def promoted_str_source() -> Iterator[str]:
    yield "a"

def promoted_delegator_bad() -> Iterator[int]:
    yield from promoted_str_source()    # ERROR: str source where int declared


_ERRORS = """
17:10: Generator declared as yielding 'int' cannot yield a value of type 'str object'
25:10: Generator declared as yielding 'int' cannot yield a value of type 'bytes object'
32:14: Generator declared as yielding 'int' cannot yield a value of type 'str object'
43:34: Generator declared as yielding 'int' cannot delegate to a generator yielding 'str object'
"""
