my_fused_type = cython.fused_type(cython.int, cython.float)


@cython.cfunc
def func(a: cython.pointer[my_fused_type]):
    print(a[0])

def main():
    a: cython.int = 3
    b: cython.float = 5.0

    func(cython.address(a))
    func(cython.address(b))
