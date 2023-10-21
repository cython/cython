def f(f64 x):
    return x ** 2 - x

def integrate_f(f64 a, f64 b, i32 N):
    cdef i32 i
    cdef f64 s
    cdef f64 dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
