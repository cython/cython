import cython

fused_type1 = cython.fused_type(cython.f64, cython.f32)
fused_type2 = cython.fused_type(cython.f64, cython.f32)

@cython.cfunc
def cfunc(arg1: fused_type1, arg2: fused_type1):
    print("cfunc called:", cython.typeof(arg1), arg1, cython.typeof(arg2), arg2)

@cython.ccall
def cpfunc(a: fused_type1, b: fused_type2):
    print("cpfunc called:", cython.typeof(a), a, cython.typeof(b), b)

def func(a: fused_type1, b: fused_type2):
    print("func called:", cython.typeof(a), a, cython.typeof(b), b)

# called from Cython space
cfunc[cython.f64](5.0, 1.0)
cpfunc[cython.f32, cython.f64](1.0, 2.0)
# Indexing def functions in Cython code requires string names
func["f32", "f64"](1.0, 2.0)
