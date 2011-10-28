# mode: error

cdef fused my_fused_type: int a; char b

_ERRORS = u"""
fused_syntax.pyx:3:26: Expected a newline
"""
