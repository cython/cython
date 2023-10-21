ctypedef fused my_fused_type:
    i32
    f64

cdef func(my_fused_type *a):
    print(a[0])

cdef i32 b = 3
cdef f64 c = 3.0

func(&b)
func(&c)
