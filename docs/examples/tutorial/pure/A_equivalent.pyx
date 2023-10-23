cpdef i32 myfunction(i32 x, i32 y=2):
    a = x - y
    return a + x * y

fn f64 _helper(f64 a):
    return a + 1

cdef class A:
    pub i32 a, b
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    cpdef foo(self, f64 x):
        print(x + _helper(1.0))
