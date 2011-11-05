# mode: error

cimport cython
from cython import fused_type

# This is all invalid
# ctypedef foo(int) dtype1
# ctypedef foo.bar(float) dtype2
# ctypedef fused_type(foo) dtype3
dtype4 = cython.fused_type(int, long, kw=None)

# ctypedef public cython.fused_type(int, long) dtype7
# ctypedef api cython.fused_type(int, long) dtype8

int_t = cython.fused_type(short, short, int)
int2_t = cython.fused_type(int, long)
dtype9 = cython.fused_type(int2_t, int)

floating = cython.fused_type(float, double)

cdef func(floating x, int2_t y):
    print x, y

cdef float x = 10.0
cdef int y = 10
func[float](x, y)
func[float][int](x, y)
func[float, int](x)
func[float, int](x, y, y)
func(x, y=y)

ctypedef fused memslice_dtype_t:
    cython.p_int # invalid dtype
    cython.long

def f(memslice_dtype_t[:, :] a):
    pass

lambda cython.integral i: i

# This is all valid
dtype5 = fused_type(int, long, float)
dtype6 = cython.fused_type(int, long)
func[float, int](x, y)

cdef fused fused1:
    int
    long long

ctypedef fused fused2:
    int
    long long

func(x, y)

_ERRORS = u"""
fused_types.pyx:10:15: fused_type does not take keyword arguments
fused_types.pyx:15:38: Type specified multiple times
fused_types.pyx:17:33: Cannot fuse a fused type
fused_types.pyx:26:4: Invalid use of fused types, type cannot be specialized
fused_types.pyx:26:4: Not enough types specified to specialize the function, int2_t is still fused
fused_types.pyx:27:4: Invalid use of fused types, type cannot be specialized
fused_types.pyx:27:4: Not enough types specified to specialize the function, int2_t is still fused
fused_types.pyx:28:16: Call with wrong number of arguments (expected 2, got 1)
fused_types.pyx:29:16: Call with wrong number of arguments (expected 2, got 3)
fused_types.pyx:30:4: Invalid use of fused types, type cannot be specialized
fused_types.pyx:30:4: Keyword and starred arguments not allowed in cdef functions.
fused_types.pyx:36:6: Invalid base type for memoryview slice: int *
fused_types.pyx:39:0: Fused lambdas not allowed
"""
