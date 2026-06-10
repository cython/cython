# mode: error
# tag: ccall,cpdef,dunders,cclass
"""
Error cases for @ccall on dunder methods inside cdef classes.
"""
import cython
from cython import cclass


# ---------------------------------------------------------------------------
# (a) @ccall on non-whitelisted dunders inside a cclass
# ---------------------------------------------------------------------------

@cclass
class MyClass1:
    @cython.ccall
    def __repr__(self) -> str:      # __repr__ is not in CPDEF_PROMOTABLE_SPECIAL_METHODS
        return "MyClass1()"

    @cython.ccall
    def __str__(self) -> str:       # __str__ is not promotable
        return "MyClass1"

    @cython.ccall
    def __hash__(self) -> int:      # __hash__ is not promotable
        return 0


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

_ERRORS = """
16:4: @ccall is not supported for dunder method '__repr__'; only whitelisted operator/richcmp dunders may be declared ccall
20:4: @ccall is not supported for dunder method '__str__'; only whitelisted operator/richcmp dunders may be declared ccall
24:4: @ccall is not supported for dunder method '__hash__'; only whitelisted operator/richcmp dunders may be declared ccall
40:19: Cannot convert 'NotImplemented' to return type 'int'
46:19: Cannot convert 'NotImplemented' to return type 'int'
"""
