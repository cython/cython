# mode: error

cimport cython

ctypedef cython.fused_type(i32, f32) fused_t

_ERRORS = u"""
fused_syntax_ctypedef.pyx:5:37: Syntax error in ctypedef statement
"""
