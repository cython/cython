.. highlight:: cython

.. _memoryviews:

**************************
Typed Memoryviews
**************************

Typed memoryviews can be used for efficient access to buffers, such as NumPy arrays, without incurring any Python overhead.
It is similar to the current buffer support (``np.ndarray[np.float64_t, ndim=2]``, but has more features and cleaner syntax.
A memoryview can be used in any context (function parameters, module-level, cdef class attribute, etc)
and can be obtained from any object that exposes the PEP 3118 buffer interface.

.. Note:: Support is experimental and new in this release, there may be bugs!

Memoryview slices
====================

Copying
--------

Memoryview slices can be obtained as follows::

    cdef int[:, :] myslice = obj

The memoryview slice can then be efficiently indexed and sliced in GIL and nogil mode.
In GIL mode these slices can also be transposed (which gives a new memoryview slice), or
copied to a C or Fortran contiguous array::

    # This slice is C contiguous
    cdef int[:, ::1] c_contiguous_slice = myslice.copy()

    # This slice is Fortran contiguous
    cdef int[::1, :] f_contiguous_slice = myslice.copy_fortran()

    print c_contiguous_slice.is_c_contig()
    print f_contiguous_slice.is_f_contig()

The `::1` in the slice type specification indicates in which dimension the data is contiguous.
It can only be used to specify full C or Fortran contiguity.

Slices can also be copied inplace::

    cdef int[:, :, :] to_slice, from_slice
    ...

    # copy the elements in from_slice to to_slice
    to_slice[...] = from_slice

.. Note:: Copying of buffers with ``object`` as the base type is not supported yet.
          Pointer types are not at all supported yet in memoryview slices.

Indexing and Slicing
--------------------

Indexing and slicing can be done with or without the GIL. It basically works like numpy. If
indices are specified for every dimension you will get specify an element of the base type
(e.g. `int`), otherwise you will get a new view. An Ellipsis means you get consecutive slices
for every unspecified dimension::

    cdef int[:, :, :] slice = ...

    # These are all equivalent
    slice[10]
    slice[10, :, :]
    slice[10, ...]

Transposing
-----------

If all dimensions are direct (i.e., there are no indirections through pointers), then
the slice can be transposed in the same way that numpy slices can be transposed::

    cdef int[:, ::1] c_contig = ...
    cdef int[::1, :] f_contig = c_contig.T

This gives a new, transposed, view on the data.

Specifying data layout
======================

Data layout can be specified using the previously seen ``::1`` slice syntax, or by using any
of the constants in ``cython.view``.
The concepts are as follows: there is data access and data packing. Data access means either
direct (no pointer) or indirect (pointer).
Data packing means your data may be strided (e.g. after slicing it, ``a[::2]``) or contiguous
(consecutive elements are adjacent in memory). If no specifier is given in any dimension,
then the data access is assumed to be direct, and the data packing assumed to be strided.
If you don't know whether a dimension will be direct or indirect (because you're getting an object
with a buffer interface from some library perhaps), then you can specify the `generic` flag,
in which case it will be determined at runtime.

The flags are as follows:

* generic - strided and direct or indirect
* strided - strided and direct (this is the default)
* indirect - strided and indirect
* contiguous - contiguous and direct
* indirect_contiguous - the list of pointers is contiguous

and they can be used like this::

    from cython cimport view

    # direct access in both dimensions, strided in the first dimension, contiguous in the last
    cdef int[:, ::view.contiguous] a

    # contiguous list of pointers to contiguous lists of ints
    cdef int[::view.indirect_contiguous, ::1] b

    # direct or indirect in the first dimension, direct in the second dimension
    # strided in both dimensions
    cdef int[::view.generic, :] c

Only the first, last or the dimension following an indirect dimension may be specified contiguous::

    # INVALID
    cdef int[::view.contiguous, ::view.indirect, :] a
    cdef int[::1, ::view.indirect, :] b

    # VALID
    cdef int[::view.indirect, ::1, :] a
    cdef int[::view.indirect, :, ::1] b
    cdef int[::view.indirect_contiguous, ::1, :]

The difference between the `contiguous` flag and the `::1` specifier is that the former specifies
contiguity for only one dimension, whereas the latter specifies contiguity for all following (Fortran) or
preceding (C) dimensions::

    cdef int[:, ::1] c_contig = ...

    # VALID
    cdef int[:, ::view.contiguous] myslice = c_contig[::2]

    # INVALID
    cdef int[:, ::1] myslice = c_contig[::2]

The former case is valid because the last dimension remains contiguous, but the first dimension
does not "follow" the last one anymore (meaning, it was strided already, but it is not C or Fortran
contiguous any longer), since it was sliced.


Memoryview Objects and Cython Arrays
====================================
These typed slices can be converted to Python objects (`cython.view.memoryview`), and are indexable,
slicable and transposable in the same way that the slices are. They can also be converted back to typed
slices at any time.

They have the following attributes:

    * shape
    * strides
    * suboffsets
    * ndim
    * size
    * itemsize
    * nbytes
    * base

And of course the aforementioned ``T`` attribute. These attributes have the same semantics as in NumPy_.
For instance, to retrieve the original object::

    import numpy
    cimport numpy as np

    cdef np.int32_t[:] a = numpy.arange(10, dtype=numpy.int32)
    a = a[::2]

    print a, numpy.asarray(a), a.base

    # this prints: <MemoryView of 'ndarray' object> [0 2 4 6 8] [0 1 2 3 4 5 6 7 8 9]

Note that this example returns the original object from which the view was obtained, and that
the view was resliced in the meantime.

Cython Array
============
Whenever a slice is copied (using any of the `copy` or `copy_fortran` methods), you get a new
memoryview slice of a newly created cython.view.array object. This array can also be used manually,
and will automatically allocate a block of data. It can later be assigned to a C or Fortran
contiguous slice (or a strided slice). It can be used like::

    import cython.view

    my_array = cython.view.array(shape=(10, 2), itemsize=sizeof(int), format="i")
    cdef int[:, :] my_slice = my_array

It also takes an optional argument `mode` ('c' or 'fortran') and a boolean `allocate_buffer`, that indicates whether a buffer should be allocated and freed when it goes out of scope::

    cdef cython.view.array my_array = cython.view.array(..., mode="fortran", allocate_buffer=False)
    my_array.data = <char *> my_data_pointer

    # define a function that can deallocate the data (if needed)
    my_array.callback_free_data = free

You can also cast pointers to array, or C arrays to arrays::

    cdef cython.view.array my_array = <int[:10, :2]> my_data_pointer
    cdef cython.view.array my_array = <int[:, :]> my_c_array

Of course, you can also immediately assign a cython.view.array to a typed memoryview slice. A C array
may be assigned directly to a memoryview slice::

    cdef int[:, ::1] myslice = my_2d_c_array

The arrays are indexable and slicable from Python space just like memoryview objects, and have the same
attributes as memoryview objects.

Coercion to NumPy
=================
Memoryview (and array) objects can be coerced to a NumPy ndarray, without having to copy the data. You can
e.g. do::

    cimport numpy as np
    import numpy as np

    numpy_array = np.asarray(<np.int32_t[:10, :10]> my_pointer)

Of course, you are not restricted to using NumPy's type (such as ``np.int32_t`` here), you can use any usable type.

None Slices
===========
Although memoryview slices are not objects they can be set to None and they can be be
checked for being None as well::

    def func(double[:] myarray = None):
        print myarray is None

Unlike object attributes of extension classes, memoryview slices are not initialized
to None.

.. _NumPy: http://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#memory-layout
