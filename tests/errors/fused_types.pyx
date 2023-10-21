# mode: error
# ticket: 1772

cimport cython
from cython import fused_type

# This is all invalid
# ctypedef foo(int) dtype1
# ctypedef foo.bar(float) dtype2
# ctypedef fused_type(foo) dtype3
dtype4 = cython.fused_type(i32, i64, kw=None)

# ctypedef pub cython.fused_type(i32, i64) dtype7
# ctypedef api cython.fused_type(i32, i64) dtype8

int_t = cython.fused_type(i16, i16, i32)
int2_t = cython.fused_type(i32, i64)
dtype9 = cython.fused_type(int2_t, i32)

floating = cython.fused_type(f32, f64)

cdef func(floating x, int2_t y):
    print x, y

cdef f32 x = 10.0
cdef i32 y = 10
func[f32](x, y)
func[f32][i32](x, y)
func[f32, i32](x)
func[f32, i32](x, y, y)
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
    i32
    const i32

cdef cdef_func_with_mix_const_type(mix_const_t val):
    print(val)

cdef_func_with_mix_const_type(1)

# This is all valid
dtype5 = fused_type(i32, i64, f32)
dtype6 = cython.fused_type(i32, i64)
func[f32, i32](x, y)

cdef fused fused1:
    i32
    i128

ctypedef fused fused2:
    i32
    i128

func(x, y)

cdef floating return_type_unfindable1(cython.integral x):
    return 1.0

cpdef floating return_type_unfindable2(cython.integral x):
    return 1.0

cdef void contents_unfindable1(cython.integral x):
    z: floating = 1  # note: cdef variables also fail with an error but not by the time this test aborts
    sz = sizeof(floating)


_ERRORS = u"""
11:15: fused_type does not take keyword arguments
16:31: Type specified multiple times
27:0: Invalid use of fused types, type cannot be specialized
27:4: Not enough types specified to specialize the function, int2_t is still fused
28:0: Invalid use of fused types, type cannot be specialized
28:4: Not enough types specified to specialize the function, int2_t is still fused
29:14: Call with wrong number of arguments (expected 2, got 1)
30:14: Call with wrong number of arguments (expected 2, got 3)
37:6: Invalid base type for memoryview slice: int *
40:0: Fused lambdas not allowed
42:5: Fused types not allowed here
42:21: cdef variable 'x' declared after it is used
45:9: Fused types not allowed here
59:0: Invalid use of fused types, type cannot be specialized
59:29: ambiguous overloaded method
# Possibly duplicates the errors more often than we want
76:5: Return type is a fused type that cannot be determined from the function arguments
79:6: Return type is a fused type that cannot be determined from the function arguments
83:4: 'z' cannot be specialized since its type is not a fused argument to this function
83:4: 'z' cannot be specialized since its type is not a fused argument to this function
83:4: 'z' cannot be specialized since its type is not a fused argument to this function
84:16: Type cannot be specialized since it is not a fused argument to this function
84:16: Type cannot be specialized since it is not a fused argument to this function
84:16: Type cannot be specialized since it is not a fused argument to this function
"""
