# cython: language_level=3

cdef double f(double x) except? -2:
    return x**2-x


def integrate_f(double a, double b, int N):
    cdef int i
    s = 0.0
    dx = (b-a)/N
    for i in range(N):
        s += f(a+i*dx)
    return s * dx
