cimport cython

ctypedef fused fused_type1:
    double
    float

ctypedef fused fused_type2:
    double
    float

cdef cfunc(fused_type1 arg1, fused_type1 arg2):
    print("cfunc called:", cython.typeof(arg1), arg1, cython.typeof(arg2), arg2)


cpdef func(fused_type1 a, fused_type2 b):
    print("func called:", cython.typeof(a), a, cython.typeof(b), b)

# called from Cython space
cfunc[double](5.0, 1.0)
func[float, double](1.0, 2.0)
