Calling C functions
====================

This tutorial describes shortly what you need to know in order to call
C library functions from Cython code.  For a longer and more
comprehensive tutorial about using external C libraries, wrapping them
and handling errors, see :doc:`clibraries`.

For simplicity, let's start with a function from the standard C
library.  This does not add any dependencies to your code, and it has
the additional advantage that Cython already defines many such
functions for you. So you can just cimport and use them.

For example, let's say you need a low-level way to parse a number from
a ``char*`` value.  You could use the ``atoi()`` function, as defined
by the ``stdlib.h`` header file.  This can be done as follows::

  from libc.stdlib cimport atoi

  cdef parse_charptr_to_py_int(char* s):
      assert s is not NULL, "byte string value is NULL"
      return atoi(s)   # note: atoi() has no error detection!

You can find a complete list of these standard cimport files in
Cython's source package ``Cython/Includes/``.  It also has a complete
set of declarations for CPython's C-API.  For example, to test at C
compilation time which CPython version your code is being compiled
with, you can do this::

  from cpython.version cimport PY_VERSION_HEX

  print PY_VERSION_HEX >= 0x030200F0 # Python version >= 3.2 final

Cython also provides declarations for the C math library::

  from libc.math cimport sin

  cdef double f(double x):
      return sin(x*x)

However, this is a library that is not linked by default on some Unix-like
systems, such as Linux. In addition to cimporting the
declarations, you must configure your build system to link against the
shared library ``m``.  For distutils, it is enough to add it to the
``libraries`` parameter of the ``Extension()`` setup::

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

If you want to access C code for which Cython does not provide a ready
to use declaration, you must declare them yourself.  For example, the
above ``sin()`` function is defined as follows::

  cdef extern from "math.h":
      double sin(double)

This declares the ``sin()`` function in a way that makes it available
to Cython code and instructs Cython to generate C code that includes
the ``math.h`` header file.  The C compiler will see the original
declaration in ``math.h`` at compile time, but Cython does not parse
"math.h" and requires a separate definition.

Just like the ``sin()`` function from the math library, it is possible
to declare and call into any C library as long as the module that
Cython generates is properly linked against the shared or static
library.
Since use of pointers in C is ubiquitous, here we give a quick example of how
to call C functions whose arguments contain pointers. Suppose you have a
file in C 'C_func_file.c', which contains a function `C_func` with
the following signature::
    void C_func(double * CPointer);

where CPointer points a one-dimensional array of size N, whose data you want
to access through a numpy array.

Now assume that you write a corresponding .pxd file C_func_file.pxd to
make the function cimport-able::
    cdef extern from "C_func_file.h":
        void C_func(double *)  

Now you can access it in a :file: `.pyx` file :file: `NumpyCPointerExample.pyx`::

    from C_func_file cimport C_func
    import cython
    cimport numpy as np
    cimport numpy as np
    
    def f(N):
        np.ndarray[np.double_t, ndim=1, mode="c"] numar = np.empty((N,),dtype=np.float64)
        C_func(<cython.float64 *> numar.data)
        # followed by some manipulations of the numarray array
        return

This way, you can have access the function more or less as a regular
python function while its data and associated memory gracefully managed (allocate and
deallocate) by Numpy.