fused_type1 = cython.fused_type(cython.double, cython.float)



fused_type2 = cython.fused_type(cython.double, cython.float)


@cython.cfunc
def cfunc(arg1: fused_type1, arg2: fused_type1):
    print("cfunc called:", cython.typeof(arg1), arg1, cython.typeof(arg2), arg2)

@cython.ccall
def func(a: fused_type1, b: fused_type2):
    print("func called:", cython.typeof(a), a, cython.typeof(b), b)

# called from Cython space
cfunc[cython.double](5.0, 1.0)
func[cython.float, cython.double](1.0, 2.0)
