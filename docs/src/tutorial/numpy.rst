Using Cython with NumPy
=======================

Cython has support for fast access to NumPy arrays. To optimize code
using such arrays one must ``cimport`` the NumPy pxd file (which ships
with Cython), and declare any arrays as having the ``ndarray``
type. The data type and number of dimensions should be fixed at
compile-time and passed. For instance::

  import numpy as np
  cimport numpy as np
  def myfunc(np.ndarray[np.float64_t, ndim=2] A):
      <...>

``myfunc`` can now only be passed two-dimensional arrays containing
double precision floats, but array indexing operation is much, much faster,
making it suitable for numerical loops. Expect speed increases well
over 100 times over a pure Python loop; in some cases the speed
increase can be as high as 700 times or more. [Seljebotn09]_
contains detailed examples and benchmarks.

Fast array declarations can currently only be used with function
local variables and arguments to ``def``-style functions (not with
arguments to ``cpdef`` or ``cdef``, and neither with fields in cdef
classes or as global variables). These limitations are considered
known defects and we hope to remove them eventually.  In most
circumstances it is possible to work around these limitations rather
easily and without a significant speed penalty, as all NumPy arrays
can also be passed as untyped objects.

Array indexing is only optimized if exactly as many indices are
provided as the number of array dimensions. Furthermore, all indices
must have a native integer type. Slices and NumPy "fancy indexing" is
not optimized. Examples::
  
  def myfunc(np.ndarray[np.float64_t, ndim=1] A):
      cdef Py_ssize_t i, j
      for i in range(A.shape[0]):
          print A[i, 0] # fast
          j = 2*i
          print A[i, j] # fast
          k = 2*i
          print A[i, k] # slow, k is not typed
          print A[i][j] # slow
          print A[i,:]  # slow

``Py_ssize_t`` is a signed integer type provided by Python which
covers the same range of values as is supported as NumPy array
indices. It is the preferred type to use for loops over arrays. 

Any Cython primitive type (float, complex float and integer types) can
be passed as the array data type. For each valid dtype in the ``numpy``
module (such as ``np.uint8``, ``np.complex128``) there is a
corresponding Cython compile-time definition in the cimport-ed NumPy
pxd file with a ``_t`` suffix [#]_. Cython structs are also allowed
and corresponds to NumPy record arrays. Examples::

  cdef packed struct Point:
      np.float64_t x, y

  def f():
      cdef np.ndarray[np.complex128_t, ndim=3] a = \
          np.zeros((3,3,3), dtype=np.complex128)
      cdef np.ndarray[Point] b = np.zeros(10, 
          dtype=np.dtype([('x', np.float64),
                          ('y', np.float64)]))
      <...>

Note that ``ndim`` defaults to 1. Also note that NumPy record arrays
are by default unaligned, meaning data is packed as tightly as
possible without considering the alignment preferences of the
CPU. Such unaligned record arrays corresponds to a Cython ``packed``
struct. If one uses an aligned dtype, by passing ``align=True`` to the
``dtype`` constructor, one must drop the ``packed`` keyword on the
struct definition.

Some data types are not yet supported, like boolean arrays and string
arrays. Also data types describing data which is not in the native
endian will likely never be supported. It is however possible to
access such arrays on a lower level by casting the arrays::

  cdef np.ndarray[np.uint8, cast=True] boolarr = (x < y)
  cdef np.ndarray[np.uint32, cast=True] values = \
      np.arange(10, dtype='>i4')

Assuming one is on a little-endian system, the ``values`` array
can still access the raw bit content of the array (which must then
be reinterpreted to yield valid results on a little-endian system).

Finally, note that typed NumPy array variables in some respects behave
a little differently from untyped arrays. ``arr.shape`` is no longer a
tuple. ``arr.shape[0]`` is valid but to e.g. print the shape one must
do ``print (<object>arr).shape`` in order to "untype" the variable
first. The same is true for ``arr.data`` (which in typed mode is a C
data pointer).

There are many more options for optimizations to consider for Cython
and NumPy arrays. We again refer the interested reader to [Seljebotn09]_.

.. [#] In Cython 0.11.2, ``np.complex64_t`` and ``np.complex128_t``
       does not work and one must write ``complex`` or 
       ``double complex`` instead. This is fixed in 0.11.3. Cython
       0.11.1 and earlier does not support complex numbers.

.. [Seljebotn09] D. S. Seljebotn, Fast numerical computations with Cython,
   Proceedings of the 8th Python in Science Conference, 2009.
