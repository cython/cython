cdef functions
==============

Python function calls can be expensive--in Cython doubly so because
one might need to convert to and from Python objects to do the call.
In our example above, the argument is assumed to be a C double both inside f()
and in the call to it, yet a Python ``float`` object must be constructed around the
argument in order to pass it.

Therefore Cython provides a syntax for declaring a C-style function,
the cdef keyword::

  cdef double f(double) except *:
      return sin(x**2)

Some form of except-modifier should usually be added, otherwise Cython
will not be able to propagate exceptions raised in the function (or a
function it calls). Above ``except *`` is used which is always
safe. An except clause can be left out if the function returns a Python
object or if it is guaranteed that an exception will not be raised
within the function call.

A side-effect of cdef is that the function is no longer available from
Python-space, as Python wouldn't know how to call it. Using the
``cpdef`` keyword instead of cdef, a Python wrapper is also created,
so that the function is available both from Cython (fast, passing
typed values directly) and from Python (wrapping values in Python
objects).

Note also that it is no longer possible to change ``f`` at runtime.

Speedup: 45 times over pure Python.

.. figure:: htmlreport.png

  Using the ``-a`` switch to the ``cython`` command line program (or
  following a link from the Sage notebook) results in an HTML report
  of Cython code interleaved with the generated C code.  Lines are
  colored according to the level of "typedness" -- white lines
  translates to pure C without any Python API calls. This report
  is invaluable when optimizing a function for speed.
