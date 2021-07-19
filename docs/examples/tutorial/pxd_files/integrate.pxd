cdef class Function:
   cpdef evaluate(self, double x)

cpdef integrate(Function f, double a, double b, int N)
