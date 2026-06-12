# mode: error
# tag: ccall,cpdef,dunders,cclass
"""
Error cases for @ccall on dunder methods inside cdef classes.
"""
import cython
from cython import cclass


# ---------------------------------------------------------------------------
# (b) Dunder with a non-object typed return AND a 'return NotImplemented' branch.
# This is a general type error (NotImplemented cannot be converted to a C type),
# caught by the return-statement analysis -- not a dunder-specific check.
# ---------------------------------------------------------------------------

@cclass
class MyClass2:
    @cython.ccall
    def __sub__(self, other: 'MyClass2') -> cython.int:
        if not isinstance(other, MyClass2):
            return NotImplemented
        return 1

    @cython.ccall
    def __eq__(self, other) -> cython.int:
        if not isinstance(other, MyClass2):
            return NotImplemented
        return 1


# ---------------------------------------------------------------------------
# (c) cpdef __hash__ with a wrong (non-Py_hash_t) return type and a
# 'return NotImplemented' branch -- general return-statement type error.
# ---------------------------------------------------------------------------

@cclass
class MyClass3:
    @cython.ccall
    def __hash__(self) -> cython.int:
        return NotImplemented  # NotImplemented cannot convert to int

_ERRORS = """
21:19: Cannot convert 'NotImplemented' to return type 'int'
27:19: Cannot convert 'NotImplemented' to return type 'int'
40:15: Cannot convert 'NotImplemented' to return type 'Py_hash_t'
"""
