# mode: error

cimport cython
from cython import fused_type

# This is all invalid
ctypedef foo(int) dtype1
ctypedef foo.bar(float) dtype2
ctypedef fused_type(foo) dtype3
dtype4 = cython.typedef(cython.fused_type(int, long, kw=None))

ctypedef public cython.fused_type(int, long) dtype7
ctypedef api cython.fused_type(int, long) dtype8

ctypedef cython.fused_type(short, short int, int) int_t
ctypedef cython.fused_type(int, long) int2_t
ctypedef cython.fused_type(int2_t, int) dtype9

ctypedef cython.fused_type(float, double) floating

cdef func(floating x, int2_t y):
    print x, y

cdef float x = 10.0
cdef int y = 10
func[float](x, y)
func[float][int](x, y)
func[float, int](x)
func[float, int](x, y, y)
func(x, y=y)

# This is all valid
ctypedef fused_type(int, long, float) dtype5
ctypedef cython.fused_type(int, long) dtype6
func[float, int](x, y)
func(x, y)

_ERRORS = u"""
fused_types.pyx:7:13: Can only fuse types with cython.fused_type()
fused_types.pyx:8:17: Can only fuse types with cython.fused_type()
fused_types.pyx:9:20: 'foo' is not a type identifier
fused_types.pyx:10:23: fused_type does not take keyword arguments
fused_types.pyx:12:0: Fused types cannot be public or api
fused_types.pyx:13:0: Fused types cannot be public or api
fused_types.pyx:15:34: Type specified multiple times
fused_types.pyx:17:27: Cannot fuse a fused type
fused_types.pyx:26:4: Not enough types specified to specialize the function, int2_t is still fused
fused_types.pyx:27:4: Not enough types specified to specialize the function, int2_t is still fused
fused_types.pyx:28:16: Call with wrong number of arguments (expected 2, got 1)
fused_types.pyx:29:16: Call with wrong number of arguments (expected 2, got 3)
fused_types.pyx:30:4: Keyword and starred arguments not allowed in cdef functions.
"""
