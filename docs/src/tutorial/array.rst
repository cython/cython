.. _array-array:

==========================
Working with Python arrays
==========================

Python has a builtin array module supporting dynamic 1-dimensional arrays of
primitive types. It is possible to access the underlying C array of a Python
array from within Cython. At the same time they are ordinary Python objects
which can be stored in lists and serialized between processes when using
:obj:`multiprocessing`.

Compared to the manual approach with :c:func:`malloc` and :c:func:`free`, this
gives the safe and automatic memory management of Python, and compared to a
Numpy array there is no need to install a dependency, as the :obj:`array`
module is built into both Python and Cython.

Safe usage with memory views
----------------------------

.. literalinclude:: ../../examples/tutorial/array/safe_usage.pyx

NB: the import brings the regular Python array object into the namespace
while the cimport adds functions accessible from Cython.

A Python array is constructed with a type signature and sequence of
initial values. For the possible type signatures, refer to the Python
documentation for the `array module <https://docs.python.org/library/array.html>`_.

Notice that when a Python array is assigned to a variable typed as
memory view, there will be a slight overhead to construct the memory
view. However, from that point on the variable can be passed to other
functions without overhead, so long as it is typed:

.. literalinclude:: ../../examples/tutorial/array/overhead.pyx


Zero-overhead, unsafe access to raw C pointer
---------------------------------------------
To avoid any overhead and to be able to pass a C pointer to other
functions, it is possible to access the underlying contiguous array as a
pointer. There is no type or bounds checking, so be careful to use the
right type and signedness.

.. literalinclude:: ../../examples/tutorial/array/unsafe_usage.pyx

Note that any length-changing operation on the array object may invalidate the
pointer.


Cloning, extending arrays
-------------------------
To avoid having to use the array constructor from the Python module,
it is possible to create a new array with the same type as a template,
and preallocate a given number of elements. The array is initialized to
zero when requested.

.. literalinclude:: ../../examples/tutorial/array/clone.pyx

An array can also be extended and resized; this avoids repeated memory
reallocation which would occur if elements would be appended or removed
one by one.

.. literalinclude:: ../../examples/tutorial/array/resize.pyx


API reference
-------------

Data fields
~~~~~~~~~~~

::

    data.as_voidptr
    data.as_chars
    data.as_schars
    data.as_uchars
    data.as_shorts
    data.as_ushorts
    data.as_ints
    data.as_uints
    data.as_longs
    data.as_ulongs
    data.as_longlongs  # requires Python >=3
    data.as_ulonglongs  # requires Python >=3
    data.as_floats
    data.as_doubles
    data.as_pyunicodes

Direct access to the underlying contiguous C array, with given type;
e.g., ``myarray.data.as_ints``.


Functions
~~~~~~~~~
The following functions are available to Cython from the array module::

    int resize(array self, Py_ssize_t n) except -1

Fast resize / realloc. Not suitable for repeated, small increments; resizes
underlying array to exactly the requested amount.

::

    int resize_smart(array self, Py_ssize_t n) except -1

Efficient for small increments; uses growth pattern that delivers
amortized linear-time appends.

::

    cdef inline array clone(array template, Py_ssize_t length, bint zero)

Fast creation of a new array, given a template array. Type will be same as
``template``. If zero is ``True``, new array will be initialized with zeroes.

::

    cdef inline array copy(array self)

Make a copy of an array.

::

    cdef inline int extend_buffer(array self, char* stuff, Py_ssize_t n) except -1

Efficient appending of new data of same type (e.g. of same array type)
``n``: number of elements (not number of bytes!)

::

    cdef inline int extend(array self, array other) except -1

Extend array with data from another array; types must match.

::

    cdef inline void zero(array self)

Set all elements of array to zero.
