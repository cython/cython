# ticket: 276
# mode: compile

__doc__ = u"""
"""

cdef class A:
    cdef __weakref__

ctypedef public class B [type B_Type, object BObject]:
    cdef __weakref__

cdef public class C [type C_Type, object CObject]:
    cdef __weakref__

