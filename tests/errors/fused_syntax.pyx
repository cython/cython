# mode: error

cdef fused my_fused_type: i32 a; char b

_ERRORS = u"""
fused_syntax.pyx:3:26: Expected a newline
"""
