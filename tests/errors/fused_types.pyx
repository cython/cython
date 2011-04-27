# mode: error

cimport cython
from cython import fused_type

# This is all invalid
ctypedef foo(int) dtype1
ctypedef foo.bar(float) dtype2
ctypedef fused_type(foo) dtype3
dtype4 = cython.typedef(cython.fused_type(int, long, kw=None))


# This is all valid
ctypedef fused_type(int, long, float) dtype5
ctypedef cython.fused_type(int, long) dtype6

_ERRORS = u"""
fused_types.pyx:7:13: Can only fuse types with cython.fused_type()
fused_types.pyx:8:17: Can only fuse types with cython.fused_type()
fused_types.pyx:9:20: 'foo' is not a type identifier
fused_types.pyx:10:23: fused_type does not take keyword arguments
"""
