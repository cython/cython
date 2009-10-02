Calling external C functions
============================

It is perfectly OK do ``from math import sin`` to use Python's
``sin()`` function.  However, calling C's own ``sin()`` function is
substantially faster, especially in tight loops.  It can be declared
and used in Cython as follows::

  cdef extern from "math.h":
      double sin(double)

  cdef double f(double x):
      return sin(x*x)

At this point there are no longer any Python wrapper objects around
our values inside of the main for loop, and so we get an impressive
speedup to 219 times the speed of Python.

Note that the above code re-declares the function from ``math.h`` to
make it available to Cython code.  The C compiler will see the
original declaration in ``math.h`` at compile time, but Cython
does not parse "math.h" and requires a separate definition.

When calling C functions, one must take care to link in the appropriate
libraries. This can be platform-specific; the below example works on Linux
and Mac OS X::

  from distutils.core import setup
  from distutils.extension import Extension
  from Cython.Distutils import build_ext

  ext_modules=[ 
      Extension("demo",
                ["demo.pyx"], 
                libraries=["m"]) # Unix-like specific
  ]

  setup(
    name = "Demos",
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules
  )

If one uses the Sage notebook to compile Cython code, one can use a special
comment to tell Sage to link in libraries::

  #clib: m

Just like the ``sin()`` function from the math library, it is possible
to declare and call into any C library as long as the module that
Cython generates is properly linked against the shared or static
library.
