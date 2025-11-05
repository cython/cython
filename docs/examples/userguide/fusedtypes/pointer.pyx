ctypedef fused my_fused_type:
    int
    double

cdef func(my_fused_type *a):
    print(a[0])


cdef int b = 3
cdef double c = 3.0

func(&b)
func(&c)
