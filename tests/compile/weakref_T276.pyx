# ticket: t276
# mode: compile

__doc__ = u"""
"""

cdef class A:
    cdef __weakref__

ctypedef pub class B [type B_Type, object BObject]:
    cdef __weakref__

cdef pub class C [type C_Type, object CObject]:
    cdef __weakref__

