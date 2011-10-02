# mode: error

from cython.parallel import *
def psum(int n):
   cdef double sum
   cdef int i
   cdef double x,step,t1,t2
   sum=0
   step=1.0/n
   for i in prange(n,nogil=True):
       x = (i)*step
       sum+=4.0/(1.0+x*x)
   return sum*step

_ERRORS = u"""
e_cython_parallel_nogil_env.pyx:12:15: Pythonic division not allowed without gil, consider using cython.cdivision(True)
"""
