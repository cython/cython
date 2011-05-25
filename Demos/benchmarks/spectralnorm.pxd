
cimport cython

cdef inline double eval_A(double i, double j)

@cython.locals(i=long)
cdef list eval_A_times_u(list u)

@cython.locals(i=long)
cdef list eval_At_times_u(list u)

cdef list eval_AtA_times_u(list u)

@cython.locals(j=long, u_j=double, partial_sum=double)
cdef double part_A_times_u(double i, list u)

@cython.locals(j=long, u_j=double, partial_sum=double)
cdef double part_At_times_u(double i, list u)
