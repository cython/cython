my_fused_type = cython.fused_type(cython.i32, cython.f32)

@cython.cfunc
def func(a: cython.pointer(my_fused_type)):
    print(a[0])

def main():
    a: cython.i32 = 3
    b: cython.f32 = 5.0

    func(cython.address(a))
    func(cython.address(b))
