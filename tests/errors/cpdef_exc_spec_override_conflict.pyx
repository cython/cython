# cython: language_level=3
# mode: error

# (a) Widening: base noexcept, override except *
cdef class BaseNoexcept:
    cpdef int method(self) noexcept:
        return 0

cdef class ChildWidenExceptStar(BaseNoexcept):
    cpdef int method(self) except *:  # widens: base promises noexcept
        return 1

# (b) Changed value: both check, but different sentinel
cdef class BaseExceptMinus1:
    cpdef int method(self) except -1:
        return 0

cdef class ChildChangedValue(BaseExceptMinus1):
    cpdef int method(self) except -2:  # different sentinel even though both check
        return 1

# (c) Changed value under narrowing: base except? -1, override except -2
cdef class BaseExceptMaybeVal:
    cpdef int method(self) except? -1:
        return 0

cdef class ChildNarrowDiffValue(BaseExceptMaybeVal):
    cpdef int method(self) except -2:  # narrowing direction but different value
        return 1

_ERRORS = """
10:4: Exception specification of 'method' is wider than the base method (base: 'noexcept', override: 'except *'); an overriding method may not raise exceptions the base method's signature excludes.
6:4: Base method declared here
19:4: Exception specification of 'method' is wider than the base method (base: 'except -1', override: 'except -2'); an overriding method may not raise exceptions the base method's signature excludes.
15:4: Base method declared here
28:4: Exception specification of 'method' is wider than the base method (base: 'except? -1', override: 'except -2'); an overriding method may not raise exceptions the base method's signature excludes.
24:4: Base method declared here
"""
