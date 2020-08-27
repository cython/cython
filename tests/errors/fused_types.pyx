# mode: error
# ticket: 1772

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


cdef cython.floating x

cdef class Foo(object):
    cdef cython.floating attr

def outer(cython.floating f):
    def inner():
        cdef cython.floating g


# Mixing const and non-const type makes fused type ambiguous
cdef fused mix_const_t:
    int
    const int

cdef cdef_func_with_mix_const_type(mix_const_t val):
    print(val)

cdef_func_with_mix_const_type(1)


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
11:15: fused_type does not take keyword arguments
16:33: Type specified multiple times
27:0: Invalid use of fused types, type cannot be specialized
27:4: Not enough types specified to specialize the function, int2_t is still fused
28:0: Invalid use of fused types, type cannot be specialized
28:4: Not enough types specified to specialize the function, int2_t is still fused
29:16: Call with wrong number of arguments (expected 2, got 1)
30:16: Call with wrong number of arguments (expected 2, got 3)
37:6: Invalid base type for memoryview slice: int *
40:0: Fused lambdas not allowed
43:5: Fused types not allowed here
46:9: Fused types not allowed here
61:0: Invalid use of fused types, type cannot be specialized
61:29: ambiguous overloaded method
"""
