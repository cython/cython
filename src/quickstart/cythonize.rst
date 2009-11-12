Faster code by adding types
===========================

Consider the following pure Python code::

  from math import sin

  def f(x):
      return sin(x**2)

  def integrate_f(a, b, N):
      s = 0
      dx = (b-a)/N
      for i in range(N):
          s += f(a+i*dx)
      return s * dx

Simply compiling this in Cython merely gives a 5% speedup.  This is
better than nothing, but adding some static types can make a much larger
difference.

With additional type declarations, this might look like::

  from math import sin

  def f(double x):
      return sin(x**2)

  def integrate_f(double a, double b, int N):
      cdef int i
      cdef double s, dx
      s = 0
      dx = (b-a)/N
      for i in range(N):
          s += f(a+i*dx)
      return s * dx

Since the iterator variable ``i`` is typed with C semantics, the for-loop will be compiled
to pure C code.  Typing ``a``, ``s`` and ``dx`` is important as they are involved
in arithmetic withing the for-loop; typing ``b`` and ``N`` makes less of a
difference, but in this case it is not much extra work to be
consistent and type the entire function.

This results in a 24 times speedup over the pure Python version.
