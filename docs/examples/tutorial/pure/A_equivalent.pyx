cpdef int myfunction(int x, int y=2):
    a = x - y
    return a + x * y

cdef double _helper(double a):
    return a + 1

cdef class A:
    cdef public int a, b
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    cpdef foo(self, double x):
        print(x + _helper(1.0))
